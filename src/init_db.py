from core.settings import settings
from db.clickhouse.client import ClickHouseClient

from services import DBService

nodes = (
    ("9000", settings.DB_NAME),
    ("9001", settings.REPLICA_DB_NAME),
    ("9002", settings.DB_NAME),
    ("9003", settings.REPLICA_DB_NAME),
)

db_service = DBService(
    clients=[
        ClickHouseClient(
            host="localhost",
            port=node[0],
            cluster_name=settings.CLUSTER_NAME,
            db_name=node[1],
        )
        for node in nodes
    ]
)

if __name__ == "__main__":
    db_service.init_db()
