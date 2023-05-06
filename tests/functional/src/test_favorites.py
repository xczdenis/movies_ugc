from http import HTTPStatus

import pytest

from movies_ugc.api.v1.routes.favorites import NAMESPACE
from tests.functional.testdata.utils import URLMaker

url_maker = URLMaker(namespace=NAMESPACE)


@pytest.mark.asyncio
class TestGetUserFavoriteMovies:
    async def test_list_is_paginated(self, test_client):
        """
        Should return paginated list of favorite user movies.
        """
        url = url_maker.make_url("get_user_favorite_movies", user_id="223e4567-e89b-12d3-a456-426614174000")
        expected_status = HTTPStatus.OK

        response = test_client.get(url)

        assert response.status_code == expected_status
        assert hasattr(response.json(), "items")


@pytest.mark.asyncio
class TestAddMovieToFavorites:
    @pytest.mark.parametrize("method", ["get", "put"])
    async def test_method_not_allowed(self, test_client, method):
        """
        The methods except POST should not be allowed.
        """
        user_id = "223e4567-e89b-12d3-a456-426614174000"
        movie_id = "223e4567-e89b-12d3-a456-426614174000"
        url = url_maker.make_url("add_movie_to_favorites", user_id=user_id, movie_id=movie_id)
        expected_status = HTTPStatus.METHOD_NOT_ALLOWED

        response = test_client.request(method, url)

        assert response.status_code == expected_status

    async def test_add_movie_to_favorites(self, test_client):
        """
        Should add movie to favorites.
        """
        user_id = "223e4567-e89b-12d3-a456-426614174000"
        movie_id = "223e4567-e89b-12d3-a456-426614174000"
        url = url_maker.make_url("add_movie_to_favorites", user_id=user_id, movie_id=movie_id)
        expected_status = HTTPStatus.CREATED

        response = test_client.post(url)

        assert response.status_code == expected_status
        assert response.json()["user_id"] == user_id
        assert response.json()["movie_id"] == movie_id
        assert response.json()["is_favorite"] is True
