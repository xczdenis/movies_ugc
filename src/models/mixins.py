from uuid import UUID

import orjson
from pydantic import BaseModel, validator

from models.utils import orjson_dumps


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
