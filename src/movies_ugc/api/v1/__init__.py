from fastapi import APIRouter

from movies_ugc.api.v1.routes import favorites, healthcheck, movie

router_v1 = APIRouter()

router_v1.include_router(movie.router)
router_v1.include_router(favorites.router)
router_v1.include_router(healthcheck.router)
