from abc import ABC, abstractmethod

from config.types import TUserId
from internal.data_gateways.base import DataGatewayConnector
from models.data_structures.movies import FavoriteMovie


class MovieInteractionsGateway(DataGatewayConnector, ABC):
    @abstractmethod
    async def get_user_favorite_movies(self, user_id: TUserId):
        ...

    @abstractmethod
    async def add_movie_to_favorites(self, favorite_movie: FavoriteMovie):
        ...

    @abstractmethod
    async def delete_movie_from_favorites(self, favorite_movie: FavoriteMovie):
        ...
