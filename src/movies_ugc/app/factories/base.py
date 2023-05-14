from dataclasses import dataclass

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from movies_ugc.app.factories.event_producer import EventProducerFactory
from movies_ugc.app.factories.main_db import MainDBClientFactory
from movies_ugc.app.factories.movie_interactions_gateway import MovieInteractionsGatewayFactory
from movies_ugc.app.factories.movie_viewing_gateway import MovieViewingGatewayFactory
from movies_ugc.config.enums import AdapterName
from movies_ugc.config.settings import app_settings
from movies_ugc.internal.data_gateways.movie_interacions import MovieInteractionsGateway
from movies_ugc.internal.data_gateways.movie_viewing import MovieViewingGateway
from movies_ugc.internal.db import EventProducerClient, SQLDatabaseClient
from movies_ugc.utils.helpers import case_free_pop


@dataclass(slots=True)
class AppFactory:
    @classmethod
    def make_app(cls, router: APIRouter | None = None, **kwargs) -> FastAPI:
        title = case_free_pop(kwargs, "title", app_settings.PROJECT_NAME)
        debug = case_free_pop(kwargs, "debug", app_settings.DEBUG)
        app = FastAPI(
            title=title,
            docs_url="/openapi",
            openapi_url="/openapi.json",
            default_response_class=ORJSONResponse,
            debug=debug,
            **kwargs
        )
        if router:
            app.include_router(router)
        return app


@dataclass(slots=True)
class BaseStrategyMixin:
    adapter_name: str = ""


@dataclass(slots=True)
class EventProducerStrategy(BaseStrategyMixin):
    def make_event_producer(self) -> EventProducerClient:
        if self.adapter_name == AdapterName.kafka:
            return EventProducerFactory.make_kafka_event_producer()


@dataclass(slots=True)
class MainDBClientStrategy(BaseStrategyMixin):
    def make_main_db_client(self) -> SQLDatabaseClient:
        if self.adapter_name == AdapterName.mongo:
            return MainDBClientFactory.make_mongo_main_db_client()


@dataclass(slots=True)
class MovieViewingGatewayStrategy(BaseStrategyMixin):
    def make_movie_viewing_gateway(self, event_producer: EventProducerClient) -> MovieViewingGateway:
        if self.adapter_name == AdapterName.kafka:
            return MovieViewingGatewayFactory.make_kafka_movie_viewing_gateway(event_producer)


@dataclass(slots=True)
class MovieInteractionsGatewayStrategy(BaseStrategyMixin):
    def make_movie_interactions_gateway(self, **kwargs) -> MovieInteractionsGateway:
        if self.adapter_name == AdapterName.mongo:
            return MovieInteractionsGatewayFactory.make_mongo_movie_interactions_gateway(**kwargs)
