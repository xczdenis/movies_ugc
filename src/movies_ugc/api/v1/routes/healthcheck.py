from api.utils import make_rout_name
from fastapi import APIRouter

NAMESPACE = "healthcheck"

router = APIRouter(
    prefix=f"/{NAMESPACE}",
)


@router.get("/ping", name=make_rout_name(NAMESPACE, "ping"), response_description="pong")
async def ping():
    return "pong"
