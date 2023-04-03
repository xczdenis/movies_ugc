from dataclasses import dataclass
from typing import Any

import backoff
from aiokafka import AIOKafkaProducer
from jsonschema import validate
from kafka.errors import KafkaConnectionError
from loguru import logger
from orjson import orjson

from config.settings import app_settings
from internal.interfaces.db import EventProducerClient


@dataclass(slots=True)
class KafkaEventProducerClient(EventProducerClient):
    host: str
    port: int
    native_client: AIOKafkaProducer | None = None

    async def connect(self, **kwargs):
        await self.define_native_client(**kwargs)
        await self.start_native_client(**kwargs)

    async def define_native_client(self, **kwargs):
        self.native_client = await self.create_native_client(**kwargs)

    async def create_native_client(self, **kwargs) -> AIOKafkaProducer:
        return AIOKafkaProducer(
            bootstrap_servers="{host}:{port}".format(host=self.host, port=self.port),
            client_id=app_settings.PROJECT_NAME,
        )

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=8)
    async def start_native_client(self, **kwargs):
        if self.native_client is not None:
            logger.info("Connect to db: %s" % self.get_db_name())
            await self.native_client.start()

    async def close(self, **kwargs):
        logger.info("Disconnect from db: %s" % self.get_db_name())
        await self.native_client.stop()

    async def is_healthy(self, **kwargs):
        ...

    def get_db_name(self) -> str:
        return "Kafka producer {host}:{port}".format(host=self.host, port=self.port)

    async def send(self, data: dict, destination: str, **kwargs):
        key = kwargs.get("key")
        await self.native_client.send(
            topic=destination, value=self._serialize(data), key=self._serialize(key)
        )

    @staticmethod
    def _serialize(value: Any, json_schema_dict: dict | None = None):
        if json_schema_dict:
            validate(value, json_schema_dict)
        return orjson.dumps(value)
