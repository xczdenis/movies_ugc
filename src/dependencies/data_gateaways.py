from internal.interfaces.data_gateways.movie_viewing import MovieViewingGateway

movie_viewing_gateway: MovieViewingGateway | None = None


async def get_movie_viewing_gateway() -> MovieViewingGateway:
    return movie_viewing_gateway
