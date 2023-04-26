import asyncio

from adapters.db_clients.clickhouse import ClickhouseDBClient
from adapters.db_clients.kafka.event_consumer import KafkaEventConsumerClient
from adapters.etl.clickhouse.loaders import ClickhouseLoaderMovieViewing
from adapters.etl.kafka.extractors import ExtractorKafka
from adapters.etl.kafka.transformers import TransformerKafkaToClickhouseMovieViewing
from config.enums import DBTables
from config.settings import ch_settings, kafka_settings
from internal.context_managers import AsyncDatabaseClientContextManager, DatabaseClientContextManager
from internal.etl.pipeline import AsyncETLPipeline

clickhouse_client = ClickhouseDBClient.from_url(
    "clickhouse://{host}:{port}".format(host=ch_settings.CH_NODE_HOST, port=ch_settings.CH_NODE_PORT)
)

kafka_consumer = KafkaEventConsumerClient.from_url(
    "kafka://{host}:{port}".format(
        host=kafka_settings.KAFKA_CONNECTION_HOST, port=kafka_settings.KAFKA_CONNECTION_PORT
    ),
    topics=(kafka_settings.KAFKA_TOPIC_MOVIE_VIEWING,),
    group_id=DBTables.movie_viewing.value,
)
extractor = ExtractorKafka(consumer=kafka_consumer)
transformer = TransformerKafkaToClickhouseMovieViewing()
loader = ClickhouseLoaderMovieViewing(db_client=clickhouse_client, commit_callback=extractor.commit)

etl_kafka_to_clickhouse_movie_viewing = AsyncETLPipeline(
    extractor=extractor, transformer_loaders_mapping=((transformer, (loader,)),)
)


async def start_etl():
    async with AsyncDatabaseClientContextManager(db_client=kafka_consumer):
        with DatabaseClientContextManager(db_client=clickhouse_client):
            await etl_kafka_to_clickhouse_movie_viewing.run()


if __name__ == "__main__":
    asyncio.run(start_etl())
