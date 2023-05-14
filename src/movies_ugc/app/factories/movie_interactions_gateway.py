from typing import Type

from beanie import Document

from movies_ugc.adapters.data_gateways.movie_interactions import MongoMovieInteractionsGateway
from movies_ugc.adapters.db_clients.mongo import AsyncMongoDBClient
from movies_ugc.internal.data_gateways.movie_interacions import MovieInteractionsGateway


class MovieInteractionsGatewayFactory:
    @classmethod
    def make_mongo_movie_interactions_gateway(
        cls, db_client: AsyncMongoDBClient, database: str, models: list[Type[Document]]
    ) -> MovieInteractionsGateway:
        return MongoMovieInteractionsGateway(
            db_client=db_client,
            database=database,
            models=models,
        )
