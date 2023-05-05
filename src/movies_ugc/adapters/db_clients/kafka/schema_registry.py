from dataclasses import dataclass

import backoff
from httpx import ConnectError
from loguru import logger
from requests.exceptions import ConnectionError
from schema_registry.client import SchemaRegistryClient
from schema_registry.client.schema import SchemaFactory
from schema_registry.client.utils import JSON_SCHEMA_TYPE, SchemaVersion

from movies_ugc.internal.db import DatabaseClient
from movies_ugc.internal.exceptions import InternalNetworkConnectionError
from movies_ugc.utils.helpers import execute_object_function


@dataclass(slots=True)
class KafkaSchemaRegistryClient(DatabaseClient):
    host: str
    port: int
    native_client: SchemaRegistryClient | None = None

    async def connect(self, **kwargs):
        logger.info("Create db client: %s" % self.get_db_name())
        await self.define_native_client()
        logger.success("Database client for db '%s' successfully created" % self.get_db_name())

    async def define_native_client(self, **kwargs):
        self.native_client = await self.create_native_client(**kwargs)

    @backoff.on_exception(backoff.expo, Exception, max_tries=8)
    async def create_native_client(self, **kwargs) -> SchemaRegistryClient:
        return SchemaRegistryClient({"url": "http://{host}:{port}".format(host=self.host, port=self.port)})

    async def close(self, **kwargs):
        logger.info("Close db client: %s" % self.get_db_name())

    async def is_healthy(self, **kwargs):
        ...

    def get_db_name(self) -> str:
        return "kafka schema registry {host}:{port}".format(host=self.host, port=self.port)

    def schema_exists(self, name: str) -> bool:
        schemas = self.get_subjects()
        return name in schemas

    def get_subjects(self) -> str:
        return self._exec("get_subjects")

    def get_latest_version(self, subject_name: str) -> SchemaVersion | None:
        return self._exec("get_schema", subject_name)

    def register_json_schema(self, name: str, schema_str: str) -> int:
        new_schema = SchemaFactory.create_schema(schema=schema_str, schema_type=JSON_SCHEMA_TYPE)
        schema_id = self._exec("register", subject=name, schema=new_schema)
        logger.info("New schema registered successful: %s" % name)
        return schema_id

    @backoff.on_exception(backoff.expo, InternalNetworkConnectionError, max_tries=1)
    def _exec(self, func: str, *args, **kwargs):
        try:
            return execute_object_function(self.native_client, func, *args, **kwargs)
        except (ConnectionError, ConnectError):
            raise InternalNetworkConnectionError(
                "Failed to establish a connection with the server: {host}:{port}".format(
                    host=self.host, port=self.port
                )
            )
