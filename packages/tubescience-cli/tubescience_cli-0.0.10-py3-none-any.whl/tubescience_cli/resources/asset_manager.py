from pydantic import BaseModel, SecretStr


class AssetManager(BaseModel):
    base_url: str = "https://dev-api.ts.app/asset-manager/api/v1"
    api_key: SecretStr = SecretStr("")

    def Client(self, **kwargs):
        import httpx

        headers = kwargs.get("headers", {})
        headers["X-API-KEY"] = self.api_key.get_secret_value()
        kwargs["headers"] = headers
        return httpx.Client(base_url=self.base_url, headers=headers)

    def AsyncClient(self, **kwargs):
        import httpx

        headers = kwargs.get("headers", {})
        headers["X-API-KEY"] = self.api_key.get_secret_value()
        kwargs["headers"] = headers
        return httpx.AsyncClient(base_url=self.base_url, **kwargs)
