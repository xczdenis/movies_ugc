from pydantic import BaseModel

from movies_ugc.config.types import TMovieId, TUserId
from movies_ugc.models.data_structures.movies import MoviePlaybackEventType


class UserMovieMixin(BaseModel):
    user_id: TUserId
    movie_id: TMovieId


class MoviePlaybackEventRequest(UserMovieMixin):
    event_type: MoviePlaybackEventType
    playback_position: int


class CurrentPlaybackPositionRequest(UserMovieMixin):
    playback_position: int


class MovieViewingRequest(UserMovieMixin):
    viewed_seconds: int


class FavoriteBaseResponse(UserMovieMixin):
    pass


class FavoriteMarkedResponse(UserMovieMixin):
    is_favorite: bool
