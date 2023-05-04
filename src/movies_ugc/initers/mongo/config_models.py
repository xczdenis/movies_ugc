from pydantic import BaseModel, Field


class MongoBaseNode(BaseModel):
    id: int = Field(alias="_id")
    host: str


class MongoConfigServerCluster(BaseModel):
    id: str = Field(alias="_id")
    configsvr: bool
    version: int = 1
    members: list[MongoBaseNode] | None = None


class MongoShard(BaseModel):
    id: str = Field(alias="_id")
    version: int = 1
    members: list[MongoBaseNode] | None = None


class MongoCollection(BaseModel):
    name: str
    key: dict


class MongoDatabase(BaseModel):
    name: str
    collections: list[MongoCollection]


class MongoCluster(BaseModel):
    configsvr: MongoConfigServerCluster
    shards: list[MongoShard]
    databases: list[MongoDatabase]
