from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generator


class Transformer(ABC):
    @abstractmethod
    def transform(self, data) -> Generator:
        ...


class AsyncTransformer(ABC):
    @abstractmethod
    async def transform(self, data) -> AsyncGenerator:
        ...
