import httpx
from typing import Literal
from pydantic import BaseModel, SecretStr


class BrightdataAPI(BaseModel):
    base_url: str = "https://api.brightdata.com"
    api_key: SecretStr = SecretStr("")
    fb_previews_dset_id: str = "gd_m20yd6vr2glw7spay2"

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key.get_secret_value()}",
            "Content-Type": "application/json",
        }

    def Client(self, **kwargs):
        kwargs.setdefault("headers", self.headers)
        return httpx.Client(base_url=self.base_url, **kwargs)

    def AsyncClient(self, **kwargs):
        kwargs.setdefault("headers", self.headers)
        return httpx.AsyncClient(base_url=self.base_url, **kwargs)

    def request_collection(
        self,
        dataset_id: str,
        inputs: list[dict],
        type: Literal["discover_new", "url_collection"] = "url_collection",
    ):
        params = {
            "dataset_id": dataset_id,
            "type": type,
        }
        with self.Client() as client:
            r = client.post("/datasets/request_collection", params=params, json=inputs)
            r.raise_for_status()
        return r.json()
