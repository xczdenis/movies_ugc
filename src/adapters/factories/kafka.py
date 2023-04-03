from adapters.data_gateways.movie_viewing import KafkaMovieViewingGateway
from adapters.db_clients.kafka import KafkaEventProducerClient, KafkaSchemaRegistryClient
from app.factories import DatabaseClientFactory, DataGatewayFactory
from config.settings import kafka_settings
from internal.interfaces.data_gateways.movie_viewing import MovieViewingGateway
from internal.interfaces.db import EventProducerClient


class KafkaDatabaseClientFactory(DatabaseClientFactory):
    def make_event_producer(self, **kwargs) -> KafkaEventProducerClient:
        event_producer_client = KafkaEventProducerClient.from_url(
            "kafka://{host}:{port}".format(
                host=kafka_settings.KAFKA_CONNECTION_HOST, port=kafka_settings.KAFKA_CONNECTION_PORT
            )
        )
        return event_producer_client


class KafkaDataGatewayFactory(DataGatewayFactory):
    def make_movie_viewing_gateway(
        self, event_producer: EventProducerClient, **kwargs
    ) -> MovieViewingGateway:
        schema_registry_client = self.make_schema_registry_client()
        return KafkaMovieViewingGateway(
            event_producer=event_producer, schema_registry_client=schema_registry_client
        )

    @staticmethod
    def make_schema_registry_client() -> KafkaSchemaRegistryClient:
        return KafkaSchemaRegistryClient.from_url(
            "kafka://{host}:{port}".format(
                host=kafka_settings.KAFKA_SCHEMA_REGISTRY_CONNECTION_HOST,
                port=kafka_settings.KAFKA_SCHEMA_REGISTRY_CONNECTION_PORT,
            )
        )
