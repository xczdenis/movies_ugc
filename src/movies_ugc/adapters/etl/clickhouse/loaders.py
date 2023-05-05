import time
from dataclasses import dataclass
from typing import AsyncGenerator, Callable

from movies_ugc.adapters.db_clients.clickhouse import ClickhouseDBClient
from movies_ugc.config.enums import DBTables
from movies_ugc.internal.etl.loader import AsyncLoader


@dataclass(slots=True)
class ClickhouseLoaderMovieViewing(AsyncLoader):
    db_client: ClickhouseDBClient = None
    commit_callback: Callable = None
    batch_size: int = 2
    timeout_ms: int = 2000
    destination: str = f"default.{DBTables.movie_viewing.value}"

    async def load(self, data: AsyncGenerator, **kwargs):
        values = ""
        current_batch_size = 0
        raw_row = None
        start = time.time()

        async for transformed_row, raw_row in data:
            values += f"{transformed_row},"
            current_batch_size += 1

            elapsed_ms = (time.time() - start) * 1000
            remaining = self.timeout_ms - elapsed_ms

            if remaining <= 0 or current_batch_size == self.batch_size:
                await self._insert_data(values[:-1], raw_row=raw_row)
                values = ""
                current_batch_size = 0
                start = time.time()

        if values:
            await self._insert_data(values[:-1], raw_row=raw_row)

    async def _insert_data(self, values: str, **kwargs):
        query = await self._get_insert_query(values)
        self.db_client.execute(query)
        if self.commit_callback:
            await self.commit_callback(message=kwargs.get("raw_row"))

    async def _get_insert_query(self, values: str):
        db, table = await self._get_db_and_table_from_destination(self.destination)
        if table == DBTables.movie_viewing:
            return await self._qet_insert_query_movie_viewing(db, values)
        return ""

    @staticmethod
    async def _qet_insert_query_movie_viewing(db: str, values: str):
        table = DBTables.movie_viewing.value
        return f"INSERT INTO {db}.{table} (user_id, movie_id, viewed_seconds) VALUES {values}"

    @staticmethod
    async def _get_db_and_table_from_destination(destination: str):
        db, table = "default", destination
        if "." in destination:
            first_part, second_part = destination.split(".")
            if second_part:
                db, table = first_part, second_part
            else:
                table = first_part
        return db, table
