from pathlib import Path

from pydantic import BaseModel, SecretStr, field_validator


class AirbyteServer(BaseModel):
    access_token: SecretStr = SecretStr("")

    @field_validator("access_token", mode="before")
    def validate_access_token(cls, v):
        if isinstance(v, str) and len(v) < 260 and Path(v).is_file():
            v = Path(v).read_text()
        return v

    def get_client(self):
        try:
            import airbyte_api  # pyright: ignore[reportMissingImports]  # noqa: PLC0415

            c = airbyte_api.AirbyteAPI(
                security=airbyte_api.models.Security(
                    bearer_auth=self.access_token.get_secret_value(),
                ),
            )
            return c
        except ImportError:
            raise ImportError(
                "Please install the airbyte-api package to use this feature."
            )
