from functools import lru_cache

from dependencies.data_gateaways import get_movie_viewing_gateway
from fastapi import Depends
from internal.data_gateways.movie_viewing import MovieViewingGateway
from internal.services.movie_viewing import MovieViewingService


@lru_cache()
def get_movie_viewing_service(
    movie_viewing_gateway: MovieViewingGateway = Depends(get_movie_viewing_gateway),
) -> MovieViewingService:
    return MovieViewingService(movie_viewing_gateway=movie_viewing_gateway)
