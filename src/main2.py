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
    query = """INSERT INTO default.movie_viewing (id, user_id, movie_id, viewed_seconds)
                      VALUES (2, 1234, 5678, 3600);"""

    query = """show databases"""

    query = """show databases; show databases;"""

    query = """
    INSERT INTO default.movie_viewing (user_id, movie_id, viewed_seconds)
    VALUES ('111e4567-e89b-12d3-a456-426614174000', '111e4567-e89b-12d3-a456-426614174000', 1),
           ('111e4567-e89b-12d3-a456-426614174000', '111e4567-e89b-12d3-a456-426614174000', 2),
           ('111e4567-e89b-12d3-a456-426614174000', '111e4567-e89b-12d3-a456-426614174000', 10),
           ('211e4567-e89b-12d3-a456-426614174000', '111e4567-e89b-12d3-a456-426614174000', 6);
    """
    r = clickhouse_client.execute(query)
    logger.debug(r)

# from clickhouse_driver import Client
# client = Client(host='localhost')
# print('start')
# p = client.execute('SELECT * FROM movies.views_progress')
# print(p)
# print('end')
