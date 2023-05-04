from dataclasses import dataclass
from typing import Type

from adapters.data_gateways.movie_interactions import MongoMovieInteractionsGateway
from adapters.db_clients.mongo import AsyncMongoDBClient
from beanie import Document
from internal.data_gateways.movie_interacions import MovieInteractionsGateway


@dataclass
class MongoDatabaseClientFactory:
    mongo_router_host: str
    mongo_router_port: int

    def make_async_db_client(self) -> AsyncMongoDBClient:
        async_db_client = AsyncMongoDBClient.from_url(
            "mongodb://{host}:{port}".format(host=self.mongo_router_host, port=self.mongo_router_port)
        )
        return async_db_client


class MongoDataGatewayFactory:
    def make_movie_interactions_gateway(
        self, db_client: AsyncMongoDBClient, database: str, models: list[Type[Document]]
    ) -> MovieInteractionsGateway:
        return MongoMovieInteractionsGateway(
            db_client=db_client,
            database=database,
            models=models,
        )
