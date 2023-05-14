from movies_ugc.adapters.db_clients.mongo import AsyncMongoDBClient
from movies_ugc.config.settings import mongo_settings
from movies_ugc.internal.db import SQLDatabaseClient


class MainDBClientFactory:
    @classmethod
    def make_mongo_main_db_client(cls) -> SQLDatabaseClient:
        async_db_client = AsyncMongoDBClient.from_url(
            "mongodb://{host}:{port}".format(
                host=mongo_settings.MONGO_ROUTER_HOST, port=mongo_settings.MONGO_ROUTER_PORT
            )
        )
        return async_db_client
