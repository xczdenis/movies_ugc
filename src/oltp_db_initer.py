import asyncio
import os

from adapters.db_clients.kafka import KafkaMetadataClient, KafkaSchemaRegistryClient
from adapters.migrations.executors.kafka import KafkaSchemaCreator, KafkaTopicCreator
from adapters.migrations.file import FileMigrationsLoader
from config.settings import kafka_settings
from internal.interfaces.context_managers import AsyncDatabaseClientContextManager
from internal.services.migration import MigrationService


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
