from pathlib import Path

from pydantic import BaseModel, SecretBytes, field_validator


class TemporalServer(BaseModel):
    host: str = "localhost:7233"
    default_task_queue: str = "temporal-tasks"
    namespace: str = "default"
    mtls_tls_cert: SecretBytes = SecretBytes(b"")
    mtls_tls_key: SecretBytes = SecretBytes(b"")

    @field_validator("mtls_tls_cert", "mtls_tls_key", mode="before")
    def validate_mtls_tls(cls, v):
        if not v:
            return v
        if isinstance(v, bytes):
            return v
        if isinstance(v, str):
            if v.startswith("-----BEGIN"):
                return v.encode("utf-8")
            elif len(v) < 260 and Path(v).exists():
                v = Path(v)
        if isinstance(v, Path):
            return v.read_bytes()
        return v

    async def connect(self):
        from temporalio.client import Client
        from temporalio.service import TLSConfig

        client_cert = self.mtls_tls_cert.get_secret_value()
        client_key = self.mtls_tls_key.get_secret_value()

        tls_config = (
            TLSConfig(
                client_cert=client_cert,
                client_private_key=client_key,
            )
            if client_cert and client_key
            else False
        )

        client = await Client.connect(
            self.host,
            namespace=self.namespace,
            tls=tls_config,
        )

        return client

    async def Worker(self, **kwargs):
        from temporalio.worker import Worker

        client = await self.connect()
        kwargs.setdefault("task_queue", self.default_task_queue)

        return Worker(client, **kwargs)
