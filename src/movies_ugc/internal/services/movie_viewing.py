from dataclasses import dataclass

from movies_ugc.config.settings import kafka_settings
from movies_ugc.internal.data_gateways.movie_viewing import MovieViewingGateway
from movies_ugc.internal.exceptions import ValidationDataError
from movies_ugc.models.data_structures.movies import MoviePlaybackEvent, MovieViewing
from movies_ugc.utils.helpers import execute_async_object_function


@dataclass
class MovieViewingService:
    movie_viewing_gateway: MovieViewingGateway

    async def add_playback_event(self, playback_event: MoviePlaybackEvent):
        await self._insert_to_db(
            "add_playback_event",
            playback_event=playback_event,
            destination=kafka_settings.KAFKA_TOPIC_MOVIE_PLAYBACK_EVENT,
        )

    async def add_playback_position(self, playback_position: MoviePlaybackEvent):
        await self._insert_to_db(
            "add_playback_position",
            playback_position=playback_position,
            destination=kafka_settings.KAFKA_TOPIC_CURRENT_PLAYBACK_POSITION,
        )

    async def add_movie_viewing(self, movie_viewing: MovieViewing):
        await self._insert_to_db(
            "add_movie_viewing",
            movie_viewing=movie_viewing,
            destination=kafka_settings.KAFKA_TOPIC_MOVIE_VIEWING,
        )

    async def _insert_to_db(self, gateway_method: str, *args, **kwargs):
        try:
            await execute_async_object_function(
                obj=self.movie_viewing_gateway, func=gateway_method, *args, **kwargs
            )
        except ValidationDataError as e:
            raise e
