from http import HTTPStatus

from movies_ugc.api.v1.routes.healthcheck import NAMESPACE
from tests.functional.testdata.utils import URLMaker

url_maker = URLMaker(namespace=NAMESPACE)


class TestHealthcheck:
    def test_ping_should_return_pong(self, test_client):
        url = url_maker.make_url("ping")
        expected_status = HTTPStatus.OK
        expected_response = "pong"

        response = test_client.get(url)

        assert response.status_code == expected_status
        assert response.json() == expected_response
