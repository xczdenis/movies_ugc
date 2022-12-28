from dataclasses import dataclass, field

from adapters.base import sql_types, Model


@dataclass
class ViewMixin(object):
    __tablename__: str = "views_progress"

    id = sql_types.int64
    user_id = sql_types.int64
    movie_id = sql_types.int64
    rating = sql_types.float64
    movie_frame = sql_types.int64
    created = sql_types.date_time


@dataclass
class View(ViewMixin, Model):
    __table_args__: dict = field(
        default_factory=lambda: {
            # "ENGINE =": "ReplicatedMergeTree('/clickhouse/tables/shard{shard}/{table}', '{replica}')",
            # "ENGINE =": "MergeTree",
            "ENGINE =": "ReplicatedMergeTree('/clickhouse/tables/{shard}/db_uuid/{uuid}', '{replica}')",
            "PARTITION BY": "toYYYYMMDD(created)",
            "PRIMARY KEY": "(id)",
            "ORDER BY": "id",
        }
    )


# @dataclass
# class DistributedView(ViewMixin, Model):
#     __table_args__: dict = field(
#         default_factory=lambda: {
#             "is_distributed": True,
#             "ENGINE =": "Distributed('$cluster', '', $table, rand())",
#         }
#     )
