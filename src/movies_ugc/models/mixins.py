from uuid import UUID

import orjson
from models.utils import orjson_dumps
from pydantic import BaseModel, validator


class UUIDMixin(BaseModel):
    id: UUID


class StrUUIDMixin(UUIDMixin):
    @validator("id")
    def validate_uuids(cls, value):  # noqa
        if value:
            return str(value)
        return value


class OrjsonConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
