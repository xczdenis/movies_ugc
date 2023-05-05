from typing import AsyncGenerator

import orjson

from movies_ugc.internal.etl.transformer import AsyncTransformer


class TransformerKafkaToClickhouseMovieViewing(AsyncTransformer):
    async def transform(self, data: AsyncGenerator) -> AsyncGenerator:
        async for kafka_record in data:
            value = orjson.loads(kafka_record.value)
            yield (
                f"('{value['user']['id']}', '{value['movie']['id']}', {value['viewed_seconds']})",
                kafka_record,
            )
