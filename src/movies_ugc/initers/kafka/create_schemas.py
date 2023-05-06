import os

from movies_ugc.adapters.db_clients.kafka.schema_registry import KafkaSchemaRegistryClient
from movies_ugc.adapters.migrations.executors.kafka import KafkaSchemaCreator
from movies_ugc.adapters.migrations.file import FileMigrationsLoader
from movies_ugc.config.settings import kafka_settings
from movies_ugc.internal.context_managers import AsyncDatabaseClientContextManager
from movies_ugc.internal.services.migration import MigrationService


async def create_schemas():
    kafka_metadata_client = KafkaSchemaRegistryClient.from_url(
        "kafka://{host}:{port}".format(
            host=kafka_settings.KAFKA_SCHEMA_REGISTRY_HOST,
            port=kafka_settings.KAFKA_SCHEMA_REGISTRY_PORT,
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
