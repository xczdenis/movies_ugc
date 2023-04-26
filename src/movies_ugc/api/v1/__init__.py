from api.v1.routes import movie
from fastapi import APIRouter

router_v1 = APIRouter()

router_v1.include_router(movie.router)
