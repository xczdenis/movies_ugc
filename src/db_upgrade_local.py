from adapters.enums import DBDialects

from config.settings import ch_settings
from utils import get_db_client, migrate, get_databases

if __name__ == "__main__":
    for i, node_port in enumerate(ch_settings.CH_NODE_EXPOSE_PORTS):
        db_client = get_db_client(
            host=ch_settings.CH_NODE_HOST_NAME, port=node_port, is_replica=i % 2 != 0
        )
        for db_name, db_is_replica in get_databases():
            migrate(
                db_client=db_client,
                dialect=DBDialects.CLICKHOUSE,
                db_name=db_name,
                db_is_replica=db_is_replica,
                cluster_name=ch_settings.CH_CLUSTER_NAME,
            )
