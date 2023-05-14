from movies_ugc.adapters.db_clients.kafka.event_producer import KafkaEventProducerClient
from movies_ugc.config.settings import kafka_settings


class EventProducerFactory:
    @classmethod
    def make_kafka_event_producer(cls) -> KafkaEventProducerClient:
        event_producer_client = KafkaEventProducerClient.from_url(
            "kafka://{host}:{port}".format(
                host=kafka_settings.KAFKA_CONNECTION_HOST, port=kafka_settings.KAFKA_CONNECTION_PORT
            )
        )
        return event_producer_client
