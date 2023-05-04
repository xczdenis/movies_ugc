from abc import ABC, abstractmethod

from internal.data_gateways.base import DataGatewayConnector
from models.data_structures.movies import CurrentPlaybackPosition, MoviePlaybackEvent, MovieViewing


class MovieViewingGateway(DataGatewayConnector, ABC):
    @abstractmethod
    async def add_playback_event(self, playback_event: MoviePlaybackEvent, destination: str):
        ...

    @abstractmethod
    async def add_playback_position(self, playback_position: CurrentPlaybackPosition, destination: str):
        ...

    @abstractmethod
    async def add_movie_viewing(self, movie_viewing: MovieViewing, destination: str):
        ...
