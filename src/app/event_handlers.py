from fastapi import FastAPI

from app import movie_viewing_gateway
from dependencies import data_gateaways
from utils.helpers import get_all_sub_apps


def register_handlers(app: FastAPI):
    @app.on_event("startup")
    async def startup_event_handler():
        data_gateaways.movie_viewing_gateway = movie_viewing_gateway

        await movie_viewing_gateway.open()

    @app.on_event("shutdown")
    async def shutdown_event_handler():
        await movie_viewing_gateway.close()


def register_event_handlers(app: FastAPI):
    sub_apps = get_all_sub_apps(app)
    for _app in app, *sub_apps:
        register_handlers(_app)
