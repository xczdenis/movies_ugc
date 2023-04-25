from abc import ABC, abstractmethod


class Loader(ABC):
    @abstractmethod
    def load(self, data, **kwargs):
        ...


class AsyncLoader(ABC):
    @abstractmethod
    async def load(self, data, **kwargs):
        ...
