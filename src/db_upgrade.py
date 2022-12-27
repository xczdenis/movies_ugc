import json

from adapters.enums import DBDialects
from src.config.settings import ch_settings, BASE_DIR
from utils import get_db_client, migrate, get_databases

if __name__ == "__main__":
    with open(BASE_DIR / ch_settings.CH_CONFIG_PATH) as ch_config_json:
        ch_config = json.load(ch_config_json)
        ch_nodes = ch_config["cluster"]["nodes"]
        for node in ch_nodes:
            db_client = get_db_client(host=node["host"], is_replica=node["is_replica"])
            for db_name, db_is_replica in get_databases():
                migrate(
                    db_client=db_client,
                    dialect=DBDialects.CLICKHOUSE,
                    db_name=db_name,
                    cluster_name=ch_settings.CH_CLUSTER_NAME,
                    db_is_replica=db_is_replica,
                )
