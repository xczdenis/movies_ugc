from enum import Enum


class DBTables(str, Enum):
    movie_viewing = "movie_viewing"


class AdapterName(str, Enum):
    kafka = "kafka"
    mongo = "mongo"
    clickhouse = "clickhouse"
