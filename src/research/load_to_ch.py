import csv
import hashlib
import time
import uuid
from collections.abc import Iterable
from functools import lru_cache, wraps
from multiprocessing import Pool, cpu_count

from loguru import logger

from adapters.db_clients.clickhouse import ClickhouseDBClient
from config.settings import ROOT_DIR, ch_settings
from internal.context_managers import DatabaseClientContextManager
from internal.db import SQLDatabaseClient

clickhouse_client: SQLDatabaseClient = ClickhouseDBClient.from_url(
    "clickhouse://{host}:{port}".format(
        host=ch_settings.CH_NODE_HOST,
        port=ch_settings.CH_NODE_PORT,
    )
)


def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Total time of '{func.__name__}' taken: {end_time - start_time:.4f} seconds")

        return result

    return wrapper


@lru_cache
def int_to_uuid(integer):
    _int = int(integer)
    byte_str = _int.to_bytes((_int.bit_length() + 7) // 8, "big")
    sha256 = hashlib.sha256(byte_str).digest()
    return f"'{str(uuid.UUID(bytes=sha256[:16], version=5))}'"


def insert(db, table, values):
    query = get_query(db, table, values)
    execute(query)


def get_query(db, table, values):
    return f"INSERT INTO {db}.{table} (user_id, movie_id, viewed_seconds) VALUES {values}"


@profile
def execute(query):
    clickhouse_client.execute(query)


def read_from_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def get_values_from_row(row: dict):
    user_id = int_to_uuid(row["userId"])
    movie_id = int_to_uuid(row["movieId"])
    viewed_seconds = int(float(row["rating"]))

    return f"({user_id}, {movie_id}, {viewed_seconds})"


def process_rows(row):
    return get_values_from_row(row)


@profile
def get_values_from_generator(generator: Iterable, batch_size):
    with Pool(cpu_count()) as pool:
        field_values = pool.map(process_rows, (row for _, row in zip(range(batch_size), generator)))

    return ",".join(field_values)


@profile
def load_data(ch_database: str, ch_table: str, batch_size):
    generator = read_from_csv(FAKE_DATA_RATINGS)
    while True:
        field_values = get_values_from_generator(generator, batch_size)
        if field_values:
            insert(ch_database, ch_table, field_values)
        else:
            break


BATCH_SIZES = 1000000
FAKE_DATA_FOLDER = "fake_data"
FAKE_DATA_RATINGS = ROOT_DIR / FAKE_DATA_FOLDER / "ratings.csv"


if __name__ == "__main__":
    with DatabaseClientContextManager(db_client=clickhouse_client):
        load_data("default", "movie_viewing", BATCH_SIZES)
