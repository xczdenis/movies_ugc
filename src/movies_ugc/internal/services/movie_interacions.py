from dataclasses import dataclass

from movies_ugc.config.types import TUserId
from movies_ugc.internal.data_gateways.movie_interacions import MovieInteractionsGateway
from movies_ugc.models.data_structures.movies import FavoriteMovie


@dataclass
class MovieInteractionsService:
    movie_interactions_gateway: MovieInteractionsGateway

    async def get_user_favorite_movies(self, user_id: TUserId):
        return await self.movie_interactions_gateway.get_user_favorite_movies(user_id)

    async def add_movie_to_favorites(self, favorite_movie: FavoriteMovie):
        await self.movie_interactions_gateway.add_movie_to_favorites(favorite_movie)

    async def delete_movie_from_favorites(self, favorite_movie: FavoriteMovie):
        await self.movie_interactions_gateway.delete_movie_from_favorites(favorite_movie)
