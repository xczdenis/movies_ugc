from typing import Type

from beanie import Document

from movies_ugc.adapters.data_gateways.movie_interactions import MongoMovieInteractionsGateway
from movies_ugc.adapters.db_clients.mongo import AsyncMongoDBClient
from movies_ugc.config.settings import mongo_settings
from movies_ugc.internal.data_gateways.movie_interacions import MovieInteractionsGateway
from movies_ugc.internal.db import SQLDatabaseClient


class MongoMainDBClientFactory:
    @classmethod
    def make_main_db_client(cls) -> SQLDatabaseClient:
        async_db_client = AsyncMongoDBClient.from_url(
            "mongodb://{host}:{port}".format(
                host=mongo_settings.MONGO_ROUTER_HOST, port=mongo_settings.MONGO_ROUTER_PORT
            )
        )
        return async_db_client


class MongoMovieInteractionsGatewayFactory:
    @classmethod
    def make_movie_interactions_gateway(
        cls, db_client: AsyncMongoDBClient, database: str, models: list[Type[Document]]
    ) -> MovieInteractionsGateway:
        return MongoMovieInteractionsGateway(
            db_client=db_client,
            database=database,
            models=models,
        )
