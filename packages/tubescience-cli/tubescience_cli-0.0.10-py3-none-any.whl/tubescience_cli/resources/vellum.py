from pydantic import BaseModel, SecretStr


class VellumAPI(BaseModel):
    api_key: SecretStr = SecretStr("")

    def get_client(self):
        from vellum.client import Vellum

        return Vellum(api_key=self.api_key.get_secret_value())

    def get_async_client(self):
        from vellum.client import AsyncVellum

        return AsyncVellum(api_key=self.api_key.get_secret_value())
