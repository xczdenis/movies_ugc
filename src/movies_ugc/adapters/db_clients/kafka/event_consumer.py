import asyncio
from dataclasses import dataclass
from typing import AsyncGenerator

import backoff
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from config.settings import app_settings
from internal.db import EventConsumerClient
from kafka.errors import KafkaConnectionError
from loguru import logger


@dataclass(slots=True)
class KafkaEventConsumerClient(EventConsumerClient):
    host: str
    port: int
    topics: tuple[str, ...] = ()
    native_client: AIOKafkaConsumer | None = None
    group_id: str = ""

    async def connect(self, **kwargs):
        logger.info("Connect to db: %s" % self.get_db_name())
        await self.define_native_client(**kwargs)
        await self.start_native_client(**kwargs)
        logger.success("The connection to db: '%s' successfully established" % self.get_db_name())

    async def define_native_client(self, **kwargs):
        self.native_client = await self.create_native_client(**kwargs)

    async def create_native_client(self, **kwargs) -> AIOKafkaConsumer:
        return AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers="{host}:{port}".format(host=self.host, port=self.port),
            client_id=app_settings.PROJECT_NAME,
            group_id=f"{app_settings.PROJECT_NAME}-{self.group_id}",
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            consumer_timeout_ms=5000,
        )

    @backoff.on_exception(backoff.expo, KafkaConnectionError, max_tries=8)
    async def start_native_client(self, **kwargs):
        if self.native_client is not None:
            await self.native_client.start()

    async def close(self, **kwargs):
        logger.info("Disconnect from db: %s" % self.get_db_name())
        await self.native_client.stop()

    async def is_healthy(self, **kwargs):
        ...

    def get_db_name(self) -> str:
        return "Kafka consumer {host}:{port}".format(host=self.host, port=self.port)

    async def read(self, **kwargs) -> AsyncGenerator:
        timeout = self.get_consumer_timeout_ms()
        while True:
            try:
                message = await asyncio.wait_for(self.native_client.getone(), timeout)
                yield message
            except asyncio.TimeoutError:
                break

    def get_consumer_timeout_ms(self) -> int:
        return self.native_client._consumer_timeout

    async def commit(self, message: ConsumerRecord, **kwargs):
        await self.native_client.commit()
