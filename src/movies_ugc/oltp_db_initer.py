import asyncio
import os

from movies_ugc.adapters.db_clients.kafka.metadata_client import KafkaMetadataClient
from movies_ugc.adapters.db_clients.kafka.schema_registry import KafkaSchemaRegistryClient
from movies_ugc.adapters.migrations.executors.kafka import KafkaSchemaCreator, KafkaTopicCreator
from movies_ugc.adapters.migrations.file import FileMigrationsLoader
from movies_ugc.config.settings import kafka_settings
from movies_ugc.internal.context_managers import AsyncDatabaseClientContextManager
from movies_ugc.internal.services.migration import MigrationService


async def create_topics():
    kafka_metadata_client = KafkaMetadataClient.from_url(
        "kafka://{host}:{port}".format(
            host=kafka_settings.KAFKA_CONNECTION_HOST, port=kafka_settings.KAFKA_CONNECTION_PORT
        )
    )
    async with AsyncDatabaseClientContextManager(db_client=kafka_metadata_client):
        repository_path = os.path.join(kafka_settings.KAFKA_MIGRATIONS_REPOSITORY_PATH, "topics")
        migrations_loader = FileMigrationsLoader(repository_path=repository_path)
        migration_executor = KafkaTopicCreator(
            kafka_client=kafka_metadata_client, context=kafka_settings.dict()
        )
        migrations_service = MigrationService(
            migrations_loader=migrations_loader,
            migration_executor=migration_executor,
        )
        migrations_service.execute_migrations()


async def create_schemas():
    kafka_metadata_client = KafkaSchemaRegistryClient.from_url(
        "kafka://{host}:{port}".format(
            host=kafka_settings.KAFKA_SCHEMA_REGISTRY_CONNECTION_HOST,
            port=kafka_settings.KAFKA_SCHEMA_REGISTRY_CONNECTION_PORT,
        )
    )
    async with AsyncDatabaseClientContextManager(db_client=kafka_metadata_client):
        repository_path = os.path.join(kafka_settings.KAFKA_MIGRATIONS_REPOSITORY_PATH, "schema_registry")
        migrations_loader = FileMigrationsLoader(repository_path=repository_path)
        migration_executor = KafkaSchemaCreator(
            kafka_client=kafka_metadata_client, context=kafka_settings.dict()
        )
        migrations_service = MigrationService(
            migrations_loader=migrations_loader,
            migration_executor=migration_executor,
        )
        migrations_service.execute_migrations()


async def main():
    await create_topics()
    await create_schemas()


if __name__ == "__main__":
    asyncio.run(main())
