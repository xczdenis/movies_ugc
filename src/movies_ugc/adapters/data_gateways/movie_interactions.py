from typing import Type

from adapters.db_clients.mongo import AsyncMongoDBClient
from beanie import Document, init_beanie
from config.types import TUserId
from internal.data_gateways.movie_interacions import MovieInteractionsGateway
from models.data_structures.movies import FavoriteMovie
from models.mongo.movies import Favorite


class MongoMovieInteractionsGateway(MovieInteractionsGateway):
    def __init__(self, db_client: AsyncMongoDBClient, database: str, models: list[Type[Document]]):
        self.db_client = db_client
        self.database = database
        self.models = models

    async def open(self, **kwargs):
        await self.db_client.connect(**kwargs)
        await init_beanie(database=self.db_client.get_db(self.database), document_models=self.models)

    async def close(self, **kwargs):
        await self.db_client.close(**kwargs)

    async def get_user_favorite_movies(self, user_id: TUserId) -> list[Document]:
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
        # favorites_movie = Favorite.find(
        #     Favorite.user_id == favorite_movie.user.id, Favorite.movie_id == favorite_movie.movie.id
        # )
        # mongo_document = await Favorite.find_one(
        #     Favorite.user_id == favorite_movie.user.id, Favorite.movie_id == favorite_movie.movie.id
        # )
        # if mongo_document:
        #     await mongo_document.delete()
