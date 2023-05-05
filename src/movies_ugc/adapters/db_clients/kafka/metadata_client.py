from collections.abc import Iterable
from dataclasses import dataclass

import backoff
from kafka.admin import KafkaAdminClient
from loguru import logger

from movies_ugc.config.settings import app_settings
from movies_ugc.internal.db import DatabaseClient


@dataclass(slots=True)
class KafkaMetadataClient(DatabaseClient):
    host: str
    port: int
    native_client: KafkaAdminClient | None = None

    async def connect(self, **kwargs):
        await self.define_native_client()

    async def define_native_client(self, **kwargs):
        self.native_client = await self.create_native_client(**kwargs)

    @backoff.on_exception(backoff.expo, Exception, max_tries=8)
    async def create_native_client(self) -> KafkaAdminClient:
        logger.info("Connect to kafka db - %s:%s" % (self.host, self.port))
        return KafkaAdminClient(
            bootstrap_servers="{host}:{port}".format(host=self.host, port=self.port),
            client_id=app_settings.PROJECT_NAME,
        )

    async def close(self, **kwargs):
        logger.info("Close connection to kafka db - %s:%s" % (self.host, self.port))
        self.native_client.close()

    async def is_healthy(self, **kwargs):
        ...

    def get_db_name(self) -> str:
        return "Kafka {host}:{port}".format(host=self.host, port=self.port)

    def list_topics(self):
        return self.native_client.list_topics()

    def create_topics(self, new_topics: Iterable, timeout_ms: int = None, validate_only: bool = False):
        return self.native_client.create_topics(new_topics, timeout_ms, validate_only)
