from fastapi import APIRouter, Depends
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

from movies_ugc.api.dependencies.interactors import get_movie_interactions_service
from movies_ugc.api.utils import make_rout_name
from movies_ugc.api.v1.schemas.movies import LikedMovieResponse, SetScoreRequest
from movies_ugc.config.types import TMovieId, TUserId
from movies_ugc.internal.services.movie_interacions import MovieInteractionsService

NAMESPACE = "likes"

router = APIRouter(prefix=f"/{NAMESPACE}", tags=["Likes"])


@router.get(
    "/users/{user_id}",
    name=make_rout_name(NAMESPACE, "get_liked_movies"),
    response_description="A list of movies that the user has liked",
)
async def get_liked_movies(
    user_id: TUserId,
    service: MovieInteractionsService = Depends(get_movie_interactions_service),
) -> Page[LikedMovieResponse]:
    """
    Get list of movies that the user has liked.
    """
    liked_movies_from_db = await service.get_liked_movies(user_id=user_id)
    return await paginate(liked_movies_from_db)


@router.post(
    "/users/{user_id}/movies/{movie_id}",
    name=make_rout_name(NAMESPACE, "like_movie"),
    response_description="Movie score set successfully",
)
async def like_movie(
    user_id: TUserId,
    movie_id: TMovieId,
    score_request: SetScoreRequest,
    service: MovieInteractionsService = Depends(get_movie_interactions_service),
) -> LikedMovieResponse:
    """
    Set score for movie.
    """
    await service.like_movie(user_id=user_id, movie_id=movie_id, score=score_request.score)
    return LikedMovieResponse(user_id=user_id, movie_id=movie_id, score=score_request.score)
