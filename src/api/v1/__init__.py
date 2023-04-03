from fastapi import APIRouter

from api.v1.routes import movie

router_v1 = APIRouter()

router_v1.include_router(movie.router)
