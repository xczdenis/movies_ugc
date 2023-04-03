from abc import abstractmethod, ABC


class DataGatewayConnector(ABC):
    @abstractmethod
    async def open(self, **kwargs):
        ...

    @abstractmethod
    async def close(self, **kwargs):
        ...
