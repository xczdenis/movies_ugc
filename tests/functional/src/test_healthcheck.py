from http import HTTPStatus

from api.v1.routes.healthcheck import NAMESPACE


class TestHealthcheck:
    def test_ping_should_return_pong(self, test_client):
        expected_status = HTTPStatus.OK
        expected_response = "pong"

        response = test_client.get(namespace=NAMESPACE, url_name="ping")

        assert response.status_code == expected_status
        assert response.json() == expected_response
