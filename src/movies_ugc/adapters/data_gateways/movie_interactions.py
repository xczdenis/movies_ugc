from typing import Type

from beanie import Document, init_beanie
from loguru import logger

from movies_ugc.adapters.db_clients.mongo import AsyncMongoDBClient
from movies_ugc.config.types import TUserId
from movies_ugc.internal.data_gateways.movie_interacions import MovieInteractionsGateway
from movies_ugc.models.data_structures.movies import FavoriteMovie
from movies_ugc.models.mongo.movies import Favorite


class MongoMovieInteractionsGateway(MovieInteractionsGateway):
    def __init__(self, db_client: AsyncMongoDBClient, database: str, models: list[Type[Document]]):
        self.db_client = db_client
        self.database = database
        self.models = models

    async def open(self, **kwargs):
        await self.db_client.connect(**kwargs)
        logger.info("Beanie (ODM for MongoDB) initialization")
        await init_beanie(database=self.db_client.get_db(self.database), document_models=self.models)
        logger.success("Beanie (ODM for MongoDB) successfully initialized")

    async def close(self, **kwargs):
        await self.db_client.close(**kwargs)

    async def get_user_favorite_movies(self, user_id: TUserId):
        return Favorite.find(Favorite.user_id == user_id)

    async def add_movie_to_favorites(self, favorite_movie: FavoriteMovie):
        """
        Add document to collection "favorites"
        """
        mongo_document = Favorite(user_id=favorite_movie.user.id, movie_id=favorite_movie.movie.id)
        await mongo_document.insert()

    async def delete_movie_from_favorites(self, favorite_movie: FavoriteMovie):
        """
        Delete document from collection "favorites"
        """
        await Favorite.find(
            Favorite.user_id == favorite_movie.user.id, Favorite.movie_id == favorite_movie.movie.id
        ).delete()
