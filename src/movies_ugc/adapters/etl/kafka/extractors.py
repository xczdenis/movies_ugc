from dataclasses import dataclass
from typing import AsyncGenerator

from adapters.db_clients.kafka.event_consumer import KafkaEventConsumerClient
from aiokafka import ConsumerRecord
from internal.etl.extractor import AsyncExtractor


@dataclass(slots=True)
class ExtractorKafka(AsyncExtractor):
    consumer: KafkaEventConsumerClient = None

    async def extract(self, **kwargs) -> AsyncGenerator:
        async for message in self.consumer.read():
            yield message

    async def commit(self, message: ConsumerRecord, **kwargs):
        await self.consumer.commit(message, **kwargs)
