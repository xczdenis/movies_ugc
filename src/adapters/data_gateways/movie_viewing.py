from typing import Any

from jsonschema import validate
from orjson import orjson
from schema_registry.client.utils import SchemaVersion

from adapters.db_clients.kafka import KafkaSchemaRegistryClient
from adapters.mapings import topic_schema_mapping
from internal.exceptions import ValidationDataError
from internal.interfaces.data_gateways.movie_viewing import MovieViewingGateway
from internal.interfaces.db import EventProducerClient
from models.movies import CurrentPlaybackPosition, MoviePlaybackEvent, MovieViewing


class KafkaMovieViewingGateway(MovieViewingGateway):
    def __init__(
        self,
        event_producer: EventProducerClient,
        topics: list[str] | None = None,
        schemas: dict | None = None,
        schema_registry_client: KafkaSchemaRegistryClient | None = None,
    ):
        self.event_producer = event_producer
        self.topics = topics or []
        self.schemas = schemas or {}
        self.schema_registry_client = schema_registry_client

    async def open(self, **kwargs):
        await self.event_producer.connect(**kwargs)
        await self.connect_schema_registry_client(**kwargs)
        await self.init_topics()
        await self.init_schemas()

    async def connect_schema_registry_client(self, **kwargs):
        if self.schema_registry_client is not None:
            await self.schema_registry_client.connect(**kwargs)

    async def init_topics(self):
        for topic in topic_schema_mapping.keys():
            self.topics.append(topic)

    async def init_schemas(self):
        for topic in self.topics:
            self.schemas[topic] = self.get_schema_for_topic(topic)

    def get_schema_for_topic(self, topic_name: str) -> dict | None:
        schema = self.schemas.get(topic_name)
        if not schema:
            registered_schema = self.get_registered_schema_for_topic_from_db(topic_name)
            if registered_schema:
                schema = registered_schema.schema.schema
        return schema

    def get_registered_schema_for_topic_from_db(self, topic_name: str) -> SchemaVersion | None:
        if self.schema_registry_client:
            schema_name = topic_schema_mapping.get(topic_name)
            if schema_name:
                return self.schema_registry_client.get_latest_version(schema_name)
        return None

    async def close(self, **kwargs):
        await self.event_producer.close(**kwargs)
        await self.close_schema_registry_client(**kwargs)

    async def close_schema_registry_client(self, **kwargs):
        if self.schema_registry_client is not None:
            await self.schema_registry_client.close(**kwargs)

    async def add_playback_event(self, playback_event: MoviePlaybackEvent, destination: str):
        key = str(playback_event.user.id)
        await self.send(data=playback_event.dict(), topic=destination, key=key)

    async def add_playback_position(self, playback_position: CurrentPlaybackPosition, destination: str):
        key = str(playback_position.user.id)
        await self.send(data=playback_position.dict(), topic=destination, key=key)

    async def add_movie_viewing(self, movie_viewing: MovieViewing, destination: str):
        key = str(movie_viewing.user.id)
        await self.send(data=movie_viewing.dict(), topic=destination, key=key)

    async def send(self, data: dict, topic: str, key: str, force: bool = False):
        if force or self.is_right_format_for_topic(data=data, topic_name=topic):
            await self.event_producer.send(data=data, destination=topic, key=key)

    def is_right_format_for_topic(self, data: dict, topic_name: str) -> bool:
        schema_dict = self.get_schema_for_topic(topic_name)
        if schema_dict:
            self.validate_data(data, schema_dict)
            return True

        return self.schema_registry_client is None

    @staticmethod
    def pars_schema_str(schema_str: str) -> dict:
        return orjson.loads(schema_str)

    @staticmethod
    def validate_data(data: Any, schema: dict):
        try:
            validate(data, schema)
        except Exception as e:
            raise ValidationDataError(str(e.message))
