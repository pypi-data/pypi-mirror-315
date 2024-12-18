from typing import Literal

from pydantic import BaseModel, SecretStr


class RetoolRPCResource(BaseModel):
    token: SecretStr = SecretStr("")
    resource_id: str = ""
    host: str = "https://ts.app"
    environment_name: str = "production"
    polling_interval_ms: int = 1000
    log_level: Literal["debug", "info", "warn", "error"] | None = "info"

    def get_client(self):
        from retoolrpc import RetoolRPC, RetoolRPCConfig

        rpc_config = RetoolRPCConfig(
            api_token=self.token.get_secret_value(),
            host=self.host,
            resource_id=self.resource_id,
            environment_name=self.environment_name,
            polling_interval_ms=self.polling_interval_ms,
            log_level=self.log_level,
        )
        rpc = RetoolRPC(rpc_config)
        return rpc


class RetoolDBResource(BaseModel):
    host: str = "ep-damp-recipe-49732364.us-west-2.retooldb.com"
    database: str = "retool"
    user: str = "retool"
    password: SecretStr = SecretStr("")

    @property
    def connection_string(self):
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}/{self.database}?sslmode=require"


class RetoolResources(BaseModel):
    db: RetoolDBResource = RetoolDBResource()
    rpc: RetoolRPCResource = RetoolRPCResource()
