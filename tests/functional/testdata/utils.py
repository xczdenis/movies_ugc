from dataclasses import dataclass

import httpx
from starlette.testclient import TestClient

from movies_ugc.api.utils import make_rout_name
from movies_ugc.main import app


@dataclass
class APIClient:
    test_client: TestClient

    def get(self, url: str, **kwargs) -> httpx.Response:
        return self.request("get", url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        return self.request("post", url, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:
        return self.request("delete", url, **kwargs)

    def put(self, url: str, **kwargs) -> httpx.Response:
        return self.request("put", url, **kwargs)

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        return self.test_client.request(method, url, **kwargs)


@dataclass
class URLMaker:
    namespace: str

    def make_url(self, url_name: str = "", **url_params):
        rout_name = make_rout_name(self.namespace, url_name)
        return app.url_path_for(rout_name, **url_params)
