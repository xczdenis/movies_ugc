from pydantic import BaseModel, Field

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


class SetScoreRequest(BaseModel):
    score: int = Field(..., ge=0, le=10, title="Score", description="Score for movie")


class LikedMovieResponse(UserMovieMixin):
    score: int


class FavoriteMarkedResponse(UserMovieMixin):
    is_favorite: bool
