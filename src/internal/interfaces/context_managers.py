from internal.interfaces.db import DatabaseClient


class DatabaseClientContextManager:
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client

    def __enter__(self):
        self.db_client.connect()
        return self.db_client

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.db_client.close()


class AsyncDatabaseClientContextManager:
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client

    async def __aenter__(self):
        await self.db_client.connect()
        return self.db_client

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.db_client.close()
