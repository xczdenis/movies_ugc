import pytest
from fastapi.testclient import TestClient

from movies_ugc.main import app
from tests.functional.testdata.utils import APIClient


@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as fast_api_test_client:
        yield APIClient(test_client=fast_api_test_client)
