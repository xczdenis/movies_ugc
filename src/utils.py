from pprint import pprint

from adapters.base import BaseDBClient, BaseDBMigrator
from adapters.clickhouse.client import ClickHouseMigrator, ClickHouseClient
from src.config.settings import ch_settings


def get_db_client(
    host: str, port: int | None = None, is_replica: bool = False
) -> BaseDBClient:
    return ClickHouseClient(host=host, port=port, host_is_replica=is_replica)


def get_db_migrator(
    client: BaseDBClient, dialect: str, db_name: str, **kwargs
) -> BaseDBMigrator:
    return ClickHouseMigrator(client=client, dialect=dialect, db_name=db_name, **kwargs)


def get_databases():
    return (ch_settings.CH_DB_NAME, False), (ch_settings.CH_REPLICA_DB_NAME, True)


def migrate(db_client: BaseDBClient, dialect: str, db_name: str, **kwargs) -> None:
    db_migrator = get_db_migrator(
        client=db_client,
        dialect=dialect,
        db_name=db_name,
        **kwargs,
    )
    db_migrator.db_upgrade()


pprint(ch_settings.dict())
