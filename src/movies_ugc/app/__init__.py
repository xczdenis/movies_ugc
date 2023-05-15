from fastapi import FastAPI
from fastapi_pagination import add_pagination

from movies_ugc.api.v1 import router_v1
from movies_ugc.app import factories
from movies_ugc.config.enums import AdapterName
from movies_ugc.config.settings import app_settings, mongo_settings
from movies_ugc.internal.responses import ErrorResponseContent
from movies_ugc.models.mongo.movies import Favorite, Like

# Database clients strategies
event_producer_strategy = factories.EventProducerStrategy(AdapterName.kafka)
main_db_client_strategy = factories.MainDBClientStrategy(AdapterName.mongo)

# Data gateways strategies
movie_viewing_gateway_strategy = factories.MovieViewingGatewayStrategy(AdapterName.kafka)
movie_interactions_gateway_factory = factories.MovieInteractionsGatewayStrategy(AdapterName.mongo)

# Database clients
event_producer = event_producer_strategy.make_event_producer()
main_db_client = main_db_client_strategy.make_main_db_client()

# Data gateways
movie_viewing_gateway = movie_viewing_gateway_strategy.make_movie_viewing_gateway(
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
    app_factory = factories.AppFactory()

    global_app_attributes = {"responses": {**global_responses}}

    main_app = app_factory.make_app(**config, **global_app_attributes)

    app_v1 = app_factory.make_app(router=router_v1, **config, **global_app_attributes)
    add_pagination(app_v1)

    mount_sub_app(main_app, app_settings.API_V1_PREFIX, app_v1)

    return main_app
