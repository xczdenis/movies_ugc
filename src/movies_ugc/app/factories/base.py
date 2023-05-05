from dataclasses import dataclass

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from movies_ugc.app.factories.kafka import KafkaEventProducerFactory, KafkaMovieViewingGatewayFactory
from movies_ugc.app.factories.mongo import MongoMainDBClientFactory, MongoMovieInteractionsGatewayFactory
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
class BaseFactoryMixin:
    adapter_name: str = ""


@dataclass(slots=True)
class EventProducerFactory(BaseFactoryMixin):
    def make_event_producer(self) -> EventProducerClient:
        if self.adapter_name == AdapterName.kafka:
            return KafkaEventProducerFactory.make_event_producer()


class MainDBClientFactory(BaseFactoryMixin):
    def make_main_db_client(self) -> SQLDatabaseClient:
        if self.adapter_name == AdapterName.mongo:
            return MongoMainDBClientFactory.make_main_db_client()


@dataclass(slots=True)
class MovieViewingGatewayFactory(BaseFactoryMixin):
    def make_movie_viewing_gateway(self, event_producer: EventProducerClient) -> MovieViewingGateway:
        if self.adapter_name == AdapterName.kafka:
            return KafkaMovieViewingGatewayFactory.make_movie_viewing_gateway(event_producer)


@dataclass(slots=True)
class MovieInteractionsGatewayFactory(BaseFactoryMixin):
    def make_movie_interactions_gateway(self, **kwargs) -> MovieInteractionsGateway:
        if self.adapter_name == AdapterName.mongo:
            return MongoMovieInteractionsGatewayFactory.make_movie_interactions_gateway(**kwargs)
