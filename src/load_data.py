import csv
import datetime
import random
from math import ceil

from loguru import logger

from adapters.clickhouse.client import ClickHouseClient
from config.settings import olap_research_settings, ROOT_DIR

db_client = ClickHouseClient(host="localhost", port="9000")


def insert_to_db(fields_values):
    fields_str = "(id, user_id, movie_id, rating, movie_frame, created)"
    query = f"INSERT INTO default.views_progress {fields_str} VALUES {fields_values}"
    start = datetime.datetime.now()
    db_client.execute(query)
    return datetime.datetime.now() - start


BENCH_SIZE = olap_research_settings.BENCH_SIZE
FILM_MAX_LENGTH = 7200

if __name__ == "__main__":
    start = datetime.datetime.now()
    sql_duration = datetime.timedelta(0)
    with open(ROOT_DIR / olap_research_settings.FAKE_DATA_PATH, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        next(reader)

        field_values = ""
        current_bench_size = 0
        bench_start = datetime.datetime.now()
        for total_rows, row in enumerate(reader):
            frame = random.SystemRandom().randint(1, FILM_MAX_LENGTH)
            field_values += (
                f"({total_rows}, {row[0]}, {row[1]}, {row[2]}, {frame}, now()), "
            )
            if current_bench_size == BENCH_SIZE - 1:
                bench_sql_duration = insert_to_db(field_values[:-2])
                logger.info(
                    "Total rows: {rows}. Bench: {t1}; Only SQL: {t2}".format(
                        rows=total_rows,
                        t1=datetime.datetime.now() - bench_start,
                        t2=bench_sql_duration,
                    ),
                )
                sql_duration += bench_sql_duration
                current_bench_size = 0
                field_values = ""
                bench_start = datetime.datetime.now()

            current_bench_size += 1

        if field_values:
            insert_to_db(field_values[:-2])

    logger.success("------------------------------")
    logger.success("?????? ???????????? ?????????????? ??????????????????!")
    logger.success("------------------------------")

    logger.info("?????????? ??????????: %s" % ceil(total_rows / BENCH_SIZE))
    logger.info("?????????? ??????????: %s" % (total_rows + 1))
    logger.info("?????????? ?????????? ????????????????????: %s" % (datetime.datetime.now() - start))
    logger.info("???????????? SQL: %s" % sql_duration)
