import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from internal.migrations import Migration, MigrationsLoader


@dataclass
class FileMigration(Migration):
    file_path: str = ""

    @property
    def name(self):
        return self.file_path.split("/")[-1]

    @property
    def query(self):
        with open(self.file_path, "r") as f:
            return f.read()


@dataclass
class QueryMigration(Migration):
    name: str = ""
    query: str = ""


@dataclass
class FileMigrationsLoader(MigrationsLoader):
    repository_path: str | Path = ""

    def load_migrations(self) -> Iterator[FileMigration]:
        all_file_names = sorted(os.listdir(self.repository_path))
        for file_name in all_file_names:
            yield FileMigration(f"{self.repository_path}/{file_name}")


@dataclass
class SemicolonSeparatedLoader(MigrationsLoader):
    repository_path: str | Path = ""

    def load_migrations(self) -> Iterator[FileMigration]:
        all_file_names = sorted(os.listdir(self.repository_path))
        for file_name in all_file_names:
            file_path = f"{self.repository_path}/{file_name}"
            with open(file_path, "r") as f:
                migration_text = f.read()
                queries = migration_text.split(";")
                if len(queries) == 1:
                    yield FileMigration(file_path)

                for index, query in enumerate(queries):
                    query = query.strip()
                    if query:
                        yield QueryMigration(name=f"{file_name} [{index+1}]", query=query)
