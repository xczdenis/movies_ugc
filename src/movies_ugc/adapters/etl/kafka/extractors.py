from dataclasses import dataclass
from typing import AsyncGenerator

from aiokafka import ConsumerRecord

from movies_ugc.adapters.db_clients.kafka.event_consumer import KafkaEventConsumerClient
from movies_ugc.internal.etl.extractor import AsyncExtractor


@dataclass(slots=True)
class ExtractorKafka(AsyncExtractor):
    consumer: KafkaEventConsumerClient = None

    async def extract(self, **kwargs) -> AsyncGenerator:
        async for message in self.consumer.read():
            yield message

    async def commit(self, message: ConsumerRecord, **kwargs):
        await self.consumer.commit(message, **kwargs)
