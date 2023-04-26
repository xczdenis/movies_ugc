from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generator


class Extractor(ABC):
    @abstractmethod
    def extract(self, **kwargs) -> Generator:
        ...


class AsyncExtractor(ABC):
    @abstractmethod
    async def extract(self, **kwargs) -> AsyncGenerator:
        ...
