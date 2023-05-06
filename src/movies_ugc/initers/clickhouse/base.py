from movies_ugc.adapters.db_clients.clickhouse import ClickhouseDBClient
from movies_ugc.adapters.migrations.executors.sql import SQLMigrationExecutor
from movies_ugc.adapters.migrations.file import SemicolonSeparatedLoader
from movies_ugc.config.settings import ch_settings
from movies_ugc.internal.context_managers import DatabaseClientContextManager
from movies_ugc.internal.db import SQLDatabaseClient
from movies_ugc.internal.services.migration import MigrationService

clickhouse_client: SQLDatabaseClient = ClickhouseDBClient.from_url(
    "clickhouse://{host}:{port}".format(
        host=ch_settings.CH_NODE_HOST,
        port=ch_settings.CH_NODE_PORT,
    )
)


def init():
    with DatabaseClientContextManager(db_client=clickhouse_client):
        migrations_loader = SemicolonSeparatedLoader(
            repository_path=ch_settings.CH_MIGRATIONS_REPOSITORY_PATH
        )
        migration_executor = SQLMigrationExecutor(db_client=clickhouse_client, context=ch_settings.dict())
        migrations_service = MigrationService(
            migrations_loader=migrations_loader, migration_executor=migration_executor
        )
        migrations_service.execute_migrations()
