from functools import lru_cache

from movies_ugc.internal.data_gateways.movie_interacions import MovieInteractionsGateway
from movies_ugc.internal.data_gateways.movie_viewing import MovieViewingGateway

movie_viewing_gateway: MovieViewingGateway | None = None
movie_interactions_gateway: MovieInteractionsGateway | None = None


@lru_cache()
def get_movie_viewing_gateway() -> MovieViewingGateway:
    return movie_viewing_gateway


@lru_cache()
def get_movie_interactions_gateway() -> MovieInteractionsGateway:
    return movie_interactions_gateway
