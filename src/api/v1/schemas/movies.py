from uuid import UUID

from pydantic import BaseModel

from models.movies import MoviePlaybackEventType


class UserMovieMixin(BaseModel):
    user_id: UUID
    movie_id: UUID


class MoviePlaybackEventRequest(UserMovieMixin):
    event_type: MoviePlaybackEventType
    playback_position: int


class CurrentPlaybackPositionRequest(UserMovieMixin):
    playback_position: int


class MovieViewingRequest(UserMovieMixin):
    viewed_seconds: int
