from api.v1 import router_v1
from app.factories.base import (
    AppFactory,
    EventProducerFactory,
    MainDBClientFactory,
    MovieInteractionsGatewayFactory,
    MovieViewingGatewayFactory,
)
from config.enums import AdapterName
from config.settings import app_settings, mongo_settings
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from internal.responses import ErrorResponseContent
from models.mongo.movies import Favorite, Like

# Database clients factories
event_producer_factory = EventProducerFactory(AdapterName.kafka)
main_db_client_factory = MainDBClientFactory(AdapterName.mongo)

# Data gateways factories
movie_viewing_gateway_factory = MovieViewingGatewayFactory(AdapterName.kafka)
movie_interactions_gateway_factory = MovieInteractionsGatewayFactory(AdapterName.mongo)

# Database clients
event_producer = event_producer_factory.make_event_producer()
main_db_client = main_db_client_factory.make_main_db_client()

# Data gateways
movie_viewing_gateway = movie_viewing_gateway_factory.make_movie_viewing_gateway(
    event_producer=event_producer
)
movie_interactions_gateway = movie_interactions_gateway_factory.make_movie_interactions_gateway(
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
