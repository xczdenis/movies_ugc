from loguru import logger

from adapters.db_clients.clickhouse import ClickhouseDBClient
from config.settings import ch_settings
from internal.interfaces.context_managers import DatabaseClientContextManager
from internal.interfaces.db import SQLDatabaseClient

clickhouse_client: SQLDatabaseClient = ClickhouseDBClient.from_url(
    "clickhouse://{host}:{port}".format(
        host=ch_settings.CH_NODE_HOST,
        port=ch_settings.CH_NODE_PORT,
    )
)
with DatabaseClientContextManager(db_client=clickhouse_client):
    # define data to be inserted
    data = [(1, 1001, 101, 3600), (2, 1002, 102, 1800), (3, 1003, 103, 2700)]

    # define SQL query to insert data
    query = """
    INSERT INTO analytics.hourly_data (domain_name, event_time, count_views)
    VALUES ('clickhouse.com', '2019-01-01 10:00:00', 1),
           ('clickhouse.com', '2019-02-02 00:00:00', 2),
           ('clickhouse.com', '2019-02-01 00:00:00', 3),
           ('clickhouse.com', '2020-01-01 00:00:00', 6);
    """

    r = clickhouse_client.execute(query)
    logger.debug(r)
