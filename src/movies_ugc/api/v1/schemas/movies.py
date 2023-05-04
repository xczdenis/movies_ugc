from config.types import TMovieId, TUserId
from models.data_structures.movies import MoviePlaybackEventType
from pydantic import BaseModel


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
