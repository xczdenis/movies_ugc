import json
from dataclasses import dataclass, field
from enum import Enum

from kafka.admin import NewTopic
from loguru import logger
from pydantic import BaseModel

from movies_ugc.adapters.db_clients.kafka.metadata_client import KafkaMetadataClient
from movies_ugc.adapters.db_clients.kafka.schema_registry import KafkaSchemaRegistryClient
from movies_ugc.internal.migrations import Migration, MigrationExecutor
from movies_ugc.utils.text import replace_env_variables


class CleanupPolicyType(str, Enum):
    delete = "delete"
    compact = "compact"


class Topic(BaseModel):
    name: str
    num_partitions: int
    cleanup_policy: CleanupPolicyType
    min_in_sync_replicas: int
    replication_factor: int
    time_to_retain_data_ms: int

    def make_kafka_topic(self) -> NewTopic:
        return NewTopic(
            name=self.name,
            num_partitions=self.num_partitions,
            replication_factor=self.replication_factor,
        )


@dataclass(slots=True)
class KafkaTopicCreator(MigrationExecutor):
    kafka_client: KafkaMetadataClient
    context: dict | None = None

    @property
    def db_name(self) -> str:
        return self.kafka_client.get_db_name()

    def execute(self, migration: Migration):
        topic = self._make_topic_from_migration(migration)
        if not self._topic_is_exists(topic):
            self.kafka_client.create_topics((topic.make_kafka_topic(),))
            logger.info("Topic '%s' created successfully" % topic.name)

    def _make_topic_from_migration(self, migration: Migration) -> Topic:
        query = replace_env_variables(migration.query, self.context)
        return Topic.parse_raw(query)

    def _topic_is_exists(self, topic: Topic) -> bool:
        return topic.name in self.kafka_client.list_topics()


@dataclass(slots=True)
class KafkaSchemaCreator(MigrationExecutor):
    kafka_client: KafkaSchemaRegistryClient
    context: dict = field(default_factory=lambda: {})

    @property
    def db_name(self) -> str:
        return self.kafka_client.get_db_name()

    def execute(self, migration: Migration):
        schema_str = replace_env_variables(migration.query, self.context)
        schema_dict = self.parse_query(schema_str)
        schema_title = schema_dict.get("title")
        if schema_title and not self.kafka_client.schema_exists(schema_title):
            self.kafka_client.register_json_schema(name=schema_title, schema_str=schema_str)

    @staticmethod
    def parse_query(text: str) -> dict:
        return json.loads(text)
