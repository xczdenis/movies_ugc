from dataclasses import dataclass, field

from internal.db import SQLDatabaseClient
from internal.migrations import Migration, MigrationExecutor
from loguru import logger
from utils.text import replace_env_variables


@dataclass(slots=True)
class SQLMigrationExecutor(MigrationExecutor):
    db_client: SQLDatabaseClient
    context: dict = field(default_factory=lambda: {})

    @property
    def db_name(self) -> str:
        return self.db_client.get_db_name()

    def execute(self, migration: Migration):
        query = replace_env_variables(migration.query, self.context)
        migration_name = migration.name
        try:
            self.db_client.execute(query)
            logger.info("Migration completed successfully: %s" % migration_name)
        except Exception as e:
            logger.error("An error occurred while applying the migration '%s': %s" % (migration_name, e))
