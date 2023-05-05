import orjson
from pydantic import BaseModel

from movies_ugc.models.utils import orjson_dumps


class UUIDMixin(BaseModel):
    id: str


class OrjsonConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
