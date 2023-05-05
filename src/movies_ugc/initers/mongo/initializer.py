from dataclasses import dataclass

from loguru import logger

from movies_ugc.adapters.db_clients.mongo import MongoDBClient
from movies_ugc.initers.mongo.config_models import (
    MongoBaseNode,
    MongoCluster,
    MongoCollection,
    MongoDatabase,
    MongoShard,
)
from movies_ugc.initers.mongo.constants import mongo_client_base_connect_config
from movies_ugc.internal.context_managers import DatabaseClientContextManager


@dataclass
class MongoInitializer:
    config_server_client: MongoDBClient
    router_client: MongoDBClient
    mongo_cluster: MongoCluster

    def init_cluster(self):
        logger.info("Initiate MongoDB cluster")
        self.init_config_server()
        self.init_repl_set_on_shards()
        self.init_router()
        self.init_databases()

    def init_config_server(self):
        logger.info("Initiate config server")
        if self.config_server_is_initialized():
            logger.info("MongoDB config server is already initialized")
        else:
            command = "replSetInitiate"
            command_config = self.mongo_cluster.configsvr.dict(by_alias=True)
            self.execute_admin_command(self.config_server_client, command, command_config)
            logger.success("Config server successfully initiated")

    def config_server_is_initialized(self) -> bool:
        if self.config_server_client.is_healthy():
            try:
                db_names = self.config_server_client.native_client.list_database_names()
                return "config" in db_names
            except Exception as e:
                logger.debug("Failed to get db_names from MongoDB config server: %s" % e)
        return False

    @staticmethod
    def execute_admin_command(
        db_client: MongoDBClient, command: str | dict, command_config: dict | None = None
    ):
        logger.debug("Execute admin command: '%s' on server '%s'" % (command, db_client.get_host_name()))
        if db_client.is_healthy():
            try:
                response = db_client.native_client.admin.command(command, command_config)
                return response
            except Exception as e:
                logger.error(
                    "Failed to execute admin command: '%s' on server '%s'. Error: %s"
                    % (command, db_client.get_db_name(), e)
                )
        else:
            logger.error("MongoDB server '%s' is not healthy" % db_client.get_host_name())
        return None

    def init_repl_set_on_shards(self):
        logger.info("Initiate replica set on shards")
        for shard in self.mongo_cluster.shards:
            self.init_repl_set_on_shard(shard)

    def init_repl_set_on_shard(self, shard: MongoShard):
        logger.info("Initiate replica set on shard: %s" % shard.id)
        shard_db_client = self.get_db_client_for_shard(shard)
        with DatabaseClientContextManager(db_client=shard_db_client):
            if self.repl_set_on_shard_is_initialized(shard, shard_db_client):
                logger.info(
                    "Replica set on shard '%s' is already initialized on server '%s'"
                    % (shard.id, shard_db_client.get_host_name())
                )
            else:
                command = "replSetInitiate"
                command_config = shard.dict(by_alias=True)
                if self.execute_admin_command(shard_db_client, command, command_config):
                    logger.success(
                        "Replica set on shard '%s' successfully initiated on server '%s'"
                        % (shard.id, shard_db_client.get_host_name())
                    )

    def get_db_client_for_shard(self, shard: MongoShard) -> MongoDBClient:
        first_node = self.get_first_node_from_shard_members(shard)
        if first_node:
            return MongoDBClient.from_url(
                "mongodb://{host}".format(host=first_node.host),
                config=mongo_client_base_connect_config,
            )
        raise Exception("Can't get db client for shard: %s" % shard.id)

    @staticmethod
    def get_first_node_from_shard_members(shard: MongoShard) -> MongoBaseNode | None:
        if shard.members:
            return shard.members[0]
        return None

    def repl_set_on_shard_is_initialized(
        self, shard_config_object: MongoShard, shard_db_client: MongoDBClient
    ) -> bool:
        command = "replSetGetStatus"
        response = self.execute_admin_command(shard_db_client, command)
        number_shard_members_on_server = len(response.get("members") or []) if response else 0
        number_shard_members_on_shard_config = len(shard_config_object.members or [])
        return number_shard_members_on_server == number_shard_members_on_shard_config

    def init_router(self):
        logger.info("Initiate shards")
        if self.router_is_initialized():
            logger.info("All shards in cluster are already initialized")
        else:
            for shard in self.mongo_cluster.shards:
                for node in shard.members:
                    self.add_shard_node_to_router(shard, node)

    def router_is_initialized(self) -> bool:
        existing_shards = self.get_existing_shards()
        return len(existing_shards) == len(self.mongo_cluster.shards)

    def get_existing_shards(self) -> list:
        command = "listShards"
        response = self.execute_admin_command(self.router_client, command)
        return response.get("shards") or []

    def add_shard_node_to_router(self, shard: MongoShard, node: MongoBaseNode):
        shard_name = "{replica_set}/{host_port}".format(replica_set=shard.id, host_port=node.host)
        command = {"addShard": shard_name}
        self.execute_admin_command(self.router_client, command)
        logger.success(
            "Shard node '%s' successfully added to router '%s'"
            % (node.host, self.router_client.get_host_name())
        )

    def init_databases(self):
        logger.info("Initiate databases")
        for database in self.mongo_cluster.databases:
            self.init_database(database)

    def init_database(self, database: MongoDatabase):
        logger.info("Initiate database '%s'" % database.name)
        for collection in database.collections:
            self.enable_sharding_for_collection(database, collection)

    def enable_sharding_for_collection(self, database: MongoDatabase, collection: MongoCollection):
        logger.info("Enable sharding for collection '%s' in database '%s'" % (collection.name, database.name))
        command = {
            "shardCollection": "{database}.{collection}".format(
                database=database.name, collection=collection.name
            ),
            "key": collection.key,
        }
        self.execute_admin_command(self.router_client, command)
        logger.success(
            "Sharding successfully enabled in database '%s' for collection '%s'"
            % (database.name, collection.name)
        )
