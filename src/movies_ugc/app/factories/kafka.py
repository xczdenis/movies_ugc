from adapters.data_gateways.movie_viewing import KafkaMovieViewingGateway
from adapters.db_clients.kafka.event_producer import KafkaEventProducerClient
from adapters.db_clients.kafka.schema_registry import KafkaSchemaRegistryClient
from config.settings import kafka_settings
from internal.data_gateways.movie_viewing import MovieViewingGateway
from internal.db import EventProducerClient


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
