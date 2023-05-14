from movies_ugc.adapters.data_gateways.movie_viewing import KafkaMovieViewingGateway
from movies_ugc.adapters.db_clients.kafka.schema_registry import KafkaSchemaRegistryClient
from movies_ugc.config.settings import kafka_settings
from movies_ugc.internal.db import EventProducerClient


class MovieViewingGatewayFactory:
    @classmethod
    def make_kafka_movie_viewing_gateway(
        cls, event_producer: EventProducerClient
    ) -> KafkaMovieViewingGateway:
        schema_registry_client = cls.make_schema_registry_client()
        return KafkaMovieViewingGateway(
            event_producer=event_producer, schema_registry_client=schema_registry_client
        )

    @classmethod
    def make_schema_registry_client(cls) -> KafkaSchemaRegistryClient:
        return KafkaSchemaRegistryClient.from_url(
            "kafka://{host}:{port}".format(
                host=kafka_settings.KAFKA_SCHEMA_REGISTRY_HOST,
                port=kafka_settings.KAFKA_SCHEMA_REGISTRY_PORT,
            )
        )
