from movies_ugc.adapters.db_clients.mongo import MongoDBClient
from movies_ugc.config.settings import mongo_settings
from movies_ugc.initers.mongo.config_models import MongoCluster
from movies_ugc.initers.mongo.constants import mongo_client_base_connect_config
from movies_ugc.initers.mongo.initializer import MongoInitializer
from movies_ugc.internal.context_managers import DatabaseClientContextManager

mongo_config_server: MongoDBClient = MongoDBClient.from_url(
    "mongodb://{host}:{port}".format(
        host=mongo_settings.MONGO_CONFIG_SERVER_HOST,
        port=mongo_settings.MONGO_CONFIG_SERVER_PORT,
    ),
    config=mongo_client_base_connect_config,
)
mongo_router: MongoDBClient = MongoDBClient.from_url(
    "mongodb://{host}:{port}".format(
        host=mongo_settings.MONGO_ROUTER_HOST,
        port=mongo_settings.MONGO_ROUTER_PORT,
    ),
    config=mongo_client_base_connect_config,
)
mongo_cluster: MongoCluster = MongoCluster.parse_file(mongo_settings.MONGO_CLUSTER_CONFIG_PATH)
mongo_initializer = MongoInitializer(
    config_server_client=mongo_config_server,
    router_client=mongo_router,
    mongo_cluster=mongo_cluster,
)


def init():
    with DatabaseClientContextManager(db_client=mongo_config_server):
        with DatabaseClientContextManager(db_client=mongo_router):
            mongo_initializer.init_cluster()
