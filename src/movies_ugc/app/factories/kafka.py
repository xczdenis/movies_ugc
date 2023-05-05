from movies_ugc.adapters.data_gateways.movie_viewing import KafkaMovieViewingGateway
from movies_ugc.adapters.db_clients.kafka.event_producer import KafkaEventProducerClient
from movies_ugc.adapters.db_clients.kafka.schema_registry import KafkaSchemaRegistryClient
from movies_ugc.config.settings import kafka_settings
from movies_ugc.internal.data_gateways.movie_viewing import MovieViewingGateway
from movies_ugc.internal.db import EventProducerClient


class KafkaEventProducerFactory:
    @classmethod
    def make_event_producer(cls) -> KafkaEventProducerClient:
        event_producer_client = KafkaEventProducerClient.from_url(
            "kafka://{host}:{port}".format(
                host=kafka_settings.KAFKA_CONNECTION_HOST, port=kafka_settings.KAFKA_CONNECTION_PORT
            )
        )
        return event_producer_client


class KafkaMovieViewingGatewayFactory:
    @classmethod
    def make_movie_viewing_gateway(cls, event_producer: EventProducerClient) -> MovieViewingGateway:
        schema_registry_client = cls.make_schema_registry_client()
        return KafkaMovieViewingGateway(
            event_producer=event_producer, schema_registry_client=schema_registry_client
        )

    @classmethod
    def make_schema_registry_client(cls) -> KafkaSchemaRegistryClient:
        return KafkaSchemaRegistryClient.from_url(
            "kafka://{host}:{port}".format(
                host=kafka_settings.KAFKA_SCHEMA_REGISTRY_CONNECTION_HOST,
                port=kafka_settings.KAFKA_SCHEMA_REGISTRY_CONNECTION_PORT,
            )
        )
