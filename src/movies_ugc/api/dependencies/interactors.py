from functools import lru_cache

from api.dependencies.data_gateaways import get_movie_interactions_gateway, get_movie_viewing_gateway
from fastapi import Depends
from internal.data_gateways.movie_interacions import MovieInteractionsGateway
from internal.data_gateways.movie_viewing import MovieViewingGateway
from internal.services.movie_interacions import MovieInteractionsService
from internal.services.movie_viewing import MovieViewingService


@lru_cache()
def get_movie_viewing_service(
    movie_viewing_gateway: MovieViewingGateway = Depends(get_movie_viewing_gateway),
) -> MovieViewingService:
    return MovieViewingService(movie_viewing_gateway=movie_viewing_gateway)


@lru_cache()
def get_movie_interactions_service(
    movie_interactions_gateway: MovieInteractionsGateway = Depends(get_movie_interactions_gateway),
) -> MovieInteractionsService:
    return MovieInteractionsService(movie_interactions_gateway=movie_interactions_gateway)
