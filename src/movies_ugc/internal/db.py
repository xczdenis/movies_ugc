from abc import ABC, abstractmethod
from typing import Generator
from urllib.parse import parse_qs, urlparse


class DatabaseClient(ABC):
    @property
    @abstractmethod
    def host(self) -> str:
        ...

    @property
    @abstractmethod
    def port(self) -> int:
        ...

    @abstractmethod
    def get_db_name(self) -> str:
        ...

    @abstractmethod
    async def connect(self, **kwargs):
        ...

    @abstractmethod
    async def close(self, **kwargs):
        ...

    @abstractmethod
    async def is_healthy(self, **kwargs) -> bool:
        ...

    @classmethod
    def from_url(cls, url: str, **kwargs):
        """
        Return a client configured from the given URL.

        For example::

            clickhouse://user:password@localhost:9000/default
            postgres://user:password@localhost:9440/default
            kafka://user:password@localhost:9440/default
        """
        parsed_url = urlparse(url)

        init_args = {}

        cls.__add_url_attr_to_kwargs(parsed_url, "hostname", "host", init_args)
        cls.__add_url_attr_to_kwargs(parsed_url, "port", "port", init_args)
        cls.__add_url_attr_to_kwargs(parsed_url, "username", "user", init_args)
        cls.__add_url_attr_to_kwargs(parsed_url, "password", "password", init_args)
        cls.__add_url_attr_to_kwargs(parsed_url, "scheme", "scheme", init_args)

        path = parsed_url.path.replace("/", "", 1)
        if path and hasattr(cls, "database"):
            init_args["database"] = path

        for name, value in parse_qs(parsed_url.query).items():
            if not value or not len(value) or not hasattr(cls, name):
                continue

            value = value[0]

            init_args[name] = value

        for k, v in kwargs.items():
            cls.__add_attr_to_kwargs(k, v, init_args)

        return cls(**init_args)

    @classmethod
    def __add_url_attr_to_kwargs(cls, parsed_url, url_attr_name: str, cls_attr_name: str, kwargs: dict):
        if hasattr(cls, cls_attr_name):
            value = getattr(parsed_url, url_attr_name)
            cls.__add_attr_to_kwargs(cls_attr_name, value, kwargs)

    @classmethod
    def __add_attr_to_kwargs(cls, attr: str, value, kwargs: dict):
        if hasattr(cls, attr) and value is not None:
            kwargs[attr] = value


class SQLDatabaseClient(DatabaseClient, ABC):
    @abstractmethod
    async def execute(self, query: str, *args, **kwargs):
        ...


class EventProducerClient(DatabaseClient, ABC):
    @abstractmethod
    async def send(self, data: dict, destination: str, **kwargs):
        ...


class EventConsumerClient(DatabaseClient, ABC):
    @abstractmethod
    async def read(self, **kwargs) -> Generator:
        ...
