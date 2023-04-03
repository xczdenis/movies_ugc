from abc import ABC, abstractmethod
from collections.abc import Iterator


class Migration(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def query(self) -> str:
        ...


class MigrationsLoader(ABC):
    @property
    @abstractmethod
    def repository_path(self):
        ...

    @abstractmethod
    def load_migrations(self) -> Iterator[Migration]:
        ...


class MigrationExecutor(ABC):
    @property
    @abstractmethod
    def db_name(self) -> str:
        ...

    @property
    @abstractmethod
    def context(self) -> dict | None:
        ...

    @abstractmethod
    def execute(self, migration: Migration):
        ...
