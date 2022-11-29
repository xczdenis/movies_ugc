from dataclasses import dataclass
from typing import Type

from clickhouse_driver import Client

from db import models
from db.base import BaseDBClient, Model
from db.enums import DBDialects


@dataclass
class ClickHouseClient(BaseDBClient):
    dialect: str = DBDialects.CLICKHOUSE

    def connect(self):
        self.connection = Client(host=self.host, port=self.port)

    def init_db(self):
        self.create_table(self.db_name, models.View)
        self.create_table("default", models.DistributedView)

    def create_table(self, db: str, table: Type[Model]):
        table_instance = table()
        query = (
            """CREATE TABLE IF NOT EXISTS {db}.{table} {fields} {extra_args};""".format(
                db=db,
                table=table.__tablename__,
                fields=table_instance.get_sql_fields(self.dialect),
                extra_args=table_instance.get_sql_args(self.cluster_name),
            )
        )
        self.execute(query)
