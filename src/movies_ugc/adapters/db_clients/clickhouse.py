from dataclasses import dataclass

from clickhouse_driver import Client
from loguru import logger

from movies_ugc.internal.db import SQLDatabaseClient


@dataclass(slots=True)
class ClickhouseDBClient(SQLDatabaseClient):
    host: str = "localhost"
    port: int = 9000
    native_client: Client | None = None

    def connect(self, **kwargs):
        self.define_native_client()

    def define_native_client(self, **kwargs):
        self.native_client = self.create_native_client(**kwargs)

    def create_native_client(self, **kwargs) -> Client:
        logger.info("Create db client: %s" % self.get_db_name())
        return Client(host=self.host, port=self.port)

    def close(self, **kwargs):
        logger.info("Close db client: %s" % self.get_db_name())
        self.native_client.disconnect()

    def is_healthy(self, **kwargs):
        ...

    def get_db_name(self) -> str:
        return "ClickHouse client {host}:{port}".format(host=self.host, port=self.port)

    def execute(self, query: str, *args, **kwargs):
        response = self.native_client.execute(query, *args, **kwargs)
        return response
