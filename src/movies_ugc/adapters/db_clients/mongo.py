from dataclasses import dataclass, field

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from movies_ugc.internal.db import DatabaseClient, SQLDatabaseClient


@dataclass(slots=True)
class MongoDBClient(DatabaseClient):
    host: str = "localhost"
    port: int = 27017
    native_client: MongoClient | None = None
    config: dict = field(default_factory=lambda: {})

    def connect(self, **kwargs):
        self.define_native_client()

    def define_native_client(self, **kwargs):
        self.native_client = self.create_native_client(**kwargs)

    def create_native_client(self, **kwargs) -> MongoClient:
        logger.info("Create db client: %s" % self.get_db_name())
        return MongoClient("mongodb://{host}:{port}/".format(host=self.host, port=self.port), **self.config)

    def close(self, **kwargs):
        logger.info("Close db client: %s" % self.get_db_name())
        self.native_client.close()

    def is_healthy(self, **kwargs) -> bool:
        silent = kwargs.get("silent", False)
        try:
            self.native_client.admin.command("ping")
            return True
        except ConnectionFailure:
            if not silent:
                logger.error("Failed to connect to the MongoDB server: %s" % self.get_db_name())
        return False

    def get_db_name(self) -> str:
        return "MongoDB {host}".format(host=self.get_host_name())

    def get_host_name(self) -> str:
        return "{host}:{port}".format(host=self.host, port=self.port)

    def get_db(self, db_name: str):
        return self.native_client[db_name]


@dataclass(slots=True)
class AsyncMongoDBClient(SQLDatabaseClient):
    host: str = "localhost"
    port: int = 27017
    native_client: AsyncIOMotorClient | None = None
    config: dict = field(default_factory=lambda: {})

    async def connect(self, **kwargs):
        logger.info("Create db client: %s" % self.get_db_name())
        self.define_native_client()
        logger.success("Database client for db '%s' successfully created" % self.get_db_name())

    def define_native_client(self, **kwargs):
        self.native_client = self.create_native_client(**kwargs)

    def create_native_client(self, **kwargs) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            "mongodb://{host}:{port}/".format(host=self.host, port=self.port), **self.config
        )

    async def close(self, **kwargs):
        logger.info("Close db client: %s" % self.get_db_name())
        self.native_client.close()

    async def is_healthy(self, **kwargs) -> bool:
        silent = kwargs.get("silent", False)
        try:
            await self.native_client.admin.command("ping")
            return True
        except ConnectionFailure:
            if not silent:
                logger.error("Failed to connect to the MongoDB server: %s" % self.get_db_name())
        return False

    def get_db_name(self) -> str:
        return "MongoDB {host}".format(host=self.get_host_name())

    def get_host_name(self) -> str:
        return "{host}:{port}".format(host=self.host, port=self.port)

    def get_db(self, db_name: str):
        return self.native_client[db_name]

    async def execute(self, query: str, *args, **kwargs):
        ...
