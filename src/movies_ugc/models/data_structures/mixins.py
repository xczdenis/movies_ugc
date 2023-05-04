import orjson
from models.utils import orjson_dumps
from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: str


class OrjsonConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
