from fastapi import FastAPI

from adapters.factories.kafka import KafkaDatabaseClientFactory, KafkaDataGatewayFactory
from api.v1 import router_v1
from app.factories import AppFactory
from config.settings import app_settings
from internal.responses import ErrorResponseContent

db_factory = KafkaDatabaseClientFactory()
data_gateway_factory = KafkaDataGatewayFactory()

event_producer = db_factory.make_event_producer()
movie_viewing_gateway = data_gateway_factory.make_movie_viewing_gateway(event_producer=event_producer)

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

    mount_sub_app(main_app, app_settings.API_V1_PREFIX, app_v1)

    return main_app
