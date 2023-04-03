from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from config.settings import app_settings
from internal.interfaces.data_gateways.movie_viewing import MovieViewingGateway
from internal.interfaces.db import EventProducerClient
from utils.helpers import case_free_pop


@dataclass
class AppFactory:
    def make_app(self, router: APIRouter | None = None, **kwargs) -> FastAPI:
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


class DatabaseClientFactory(ABC):
    @abstractmethod
    def make_event_producer(self, **kwargs) -> EventProducerClient:
        ...


class DataGatewayFactory(ABC):
    def make_movie_viewing_gateway(
        self, event_producer: EventProducerClient, **kwargs
    ) -> MovieViewingGateway:
        ...
