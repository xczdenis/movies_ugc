from abc import abstractmethod, ABC

from internal.interfaces.data_gateways.base import DataGatewayConnector
from models.movies import MoviePlaybackEvent, CurrentPlaybackPosition, MovieViewing


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
