from adapters.factories.kafka import KafkaDatabaseClientFactory, KafkaDataGatewayFactory
from adapters.factories.mongo import MongoDatabaseClientFactory, MongoDataGatewayFactory
from api.v1 import router_v1
from app.factories import AppFactory
from config.settings import app_settings, mongo_settings
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from internal.responses import ErrorResponseContent
from models.mongo.movies import Favorite, Like

kafka_db_factory = KafkaDatabaseClientFactory()
kafka_data_gateway_factory = KafkaDataGatewayFactory()

mongo_db_factory = MongoDatabaseClientFactory(
    mongo_router_host=mongo_settings.MONGO_ROUTER_HOST, mongo_router_port=mongo_settings.MONGO_ROUTER_PORT
)
mongo_data_gateway_factory = MongoDataGatewayFactory()

event_producer = kafka_db_factory.make_event_producer()
movie_viewing_gateway = kafka_data_gateway_factory.make_movie_viewing_gateway(event_producer=event_producer)

main_db_client = mongo_db_factory.make_async_db_client()
movie_interactions_gateway = mongo_data_gateway_factory.make_movie_interactions_gateway(
    db_client=main_db_client,
    database=mongo_settings.MONGO_DB_MOVIES,
    models=[Like, Favorite],
)

global_responses = {
    500: {"model": ErrorResponseContent, "description": "Internal server error"},
    400: {"model": ErrorResponseContent, "description": "Bad request"},
}


def mount_sub_app(main_app: FastAPI, api_version_prefix: str, sub_app: FastAPI):
    main_app.mount(f"/{app_settings.BASE_API_PREFIX}/{api_version_prefix}", sub_app)


def create_app(config: dict) -> FastAPI:
    app_factory = AppFactory()

    global_app_attributes = {"responses": {**global_responses}}

    main_app = app_factory.make_app(**config, **global_app_attributes)

    app_v1 = app_factory.make_app(router=router_v1, **config, **global_app_attributes)
    add_pagination(app_v1)

    mount_sub_app(main_app, app_settings.API_V1_PREFIX, app_v1)

    return main_app
