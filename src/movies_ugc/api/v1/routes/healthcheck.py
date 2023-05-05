from fastapi import APIRouter

from movies_ugc.api.utils import make_rout_name

NAMESPACE = "healthcheck"

router = APIRouter(prefix=f"/{NAMESPACE}")


@router.get("/ping", name=make_rout_name(NAMESPACE, "ping"), response_description="pong")
async def ping():
    return "pong"
