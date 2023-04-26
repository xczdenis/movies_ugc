from collections.abc import Iterator
from dataclasses import dataclass

from internal.migrations import Migration, MigrationExecutor, MigrationsLoader
from loguru import logger


@dataclass
class MigrationService:
    migrations_loader: MigrationsLoader
    migration_executor: MigrationExecutor

    def execute_migrations(self):
        db_name = self.migration_executor.db_name
        logger.info("Apply migrations for db '%s'" % db_name)
        migrations = self.load_migrations()
        for migration in migrations:
            self.migration_executor.execute(migration)
        logger.info("All migrations for db '%s' applied successfully" % db_name)

    def load_migrations(self) -> Iterator[Migration]:
        return self.migrations_loader.load_migrations()
