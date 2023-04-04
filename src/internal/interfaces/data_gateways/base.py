from abc import ABC, abstractmethod


class DataGatewayConnector(ABC):
    @abstractmethod
    async def open(self, **kwargs):
        ...

    @abstractmethod
    async def close(self, **kwargs):
        ...
