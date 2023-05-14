from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.beanie import paginate as paginate
from fastapi_pagination.links import Page

from movies_ugc.api.dependencies.interactors import get_movie_interactions_service
from movies_ugc.api.utils import make_rout_name
from movies_ugc.api.v1.schemas.movies import FavoriteBaseResponse, FavoriteMarkedResponse
from movies_ugc.config.types import TMovieId, TUserId
from movies_ugc.internal.services.movie_interacions import MovieInteractionsService
from movies_ugc.models.data_structures.movies import FavoriteMovie, Movie
from movies_ugc.models.data_structures.users import User

NAMESPACE = "favorites"

router = APIRouter(prefix=f"/{NAMESPACE}", tags=["Favorites"])


@router.get(
    "/users/{user_id}",
    name=make_rout_name(NAMESPACE, "get_user_favorite_movies"),
    response_description="A list of favorite user movies",
)
async def get_user_favorite_movies(
    user_id: TUserId,
    service: MovieInteractionsService = Depends(get_movie_interactions_service),
) -> Page[FavoriteBaseResponse]:
    """
    Get list of favorite user movies.
    """
    favorite_movies_from_db = await service.get_user_favorite_movies(user_id=user_id)
    return await paginate(favorite_movies_from_db)


@router.post(
    "/users/{user_id}/movies/{movie_id}",
    name=make_rout_name(NAMESPACE, "add_movie_to_favorites"),
    response_description="The movie added to favorites successfully",
    status_code=HTTPStatus.CREATED,
)
async def add_movie_to_favorites(
    user_id: TUserId,
    movie_id: TMovieId,
    service: MovieInteractionsService = Depends(get_movie_interactions_service),
) -> FavoriteMarkedResponse:
    """
    Add movie to favorites.
    """
    favorite_movie = FavoriteMovie(user=User(id=user_id), movie=Movie(id=movie_id))

    await service.add_movie_to_favorites(favorite_movie=favorite_movie)
    response = FavoriteMarkedResponse(user_id=user_id, movie_id=movie_id, is_favorite=True)

    return response


@router.delete(
    "/users/{user_id}/movies/{movie_id}",
    name=make_rout_name(NAMESPACE, "delete_movie_from_favorites"),
    response_description="The movie deleted from favorites successfully",
)
async def delete_movie_from_favorites(
    user_id: TUserId,
    movie_id: TMovieId,
    service: MovieInteractionsService = Depends(get_movie_interactions_service),
) -> FavoriteMarkedResponse:
    """
    Delete movie from favorites.
    """
    favorite_movie = FavoriteMovie(user=User(id=user_id), movie=Movie(id=movie_id))

    await service.delete_movie_from_favorites(favorite_movie=favorite_movie)
    response = FavoriteMarkedResponse(user_id=user_id, movie_id=movie_id, is_favorite=False)

    return response
