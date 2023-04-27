import httpx
import pytest
from api.utils import make_rout_name
from fastapi.testclient import TestClient
from main import app


class APIClient:
    def __init__(self, native_test_client: TestClient):
        self.test_client = native_test_client

    def get(self, namespace: str, url_name: str, **kwargs) -> httpx.Response:
        url = self._make_url(namespace, url_name)
        return self.test_client.get(url, **kwargs)

    def _make_url(self, namespace: str, url_name: str):
        rout_name = make_rout_name(namespace, url_name)
        return self.test_client.app.url_path_for(rout_name)


@pytest.fixture(scope="session")
def test_client():
    fast_api_test_client = TestClient(app)
    client = APIClient(native_test_client=fast_api_test_client)
    yield client
