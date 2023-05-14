from enum import Enum

from movies_ugc.models.data_structures.mixins import OrjsonConfigMixin, UUIDMixin
from movies_ugc.models.data_structures.users import User


class MoviePlaybackEventType(str, Enum):
    play = "play"
    pause = "pause"
    stop = "stop"
    fast_forward = "fast_forward"
    rewind = "rewind"


class Movie(UUIDMixin, OrjsonConfigMixin):
    pass


class MoviePlaybackEvent(OrjsonConfigMixin):
    user: User
    movie: Movie
    event_type: MoviePlaybackEventType
    playback_position: int


class CurrentPlaybackPosition(OrjsonConfigMixin):
    user: User
    movie: Movie
    playback_position: int


class MovieViewing(OrjsonConfigMixin):
    user: User
    movie: Movie
    viewed_seconds: int


class FavoriteMovie(OrjsonConfigMixin):
    user: User
    movie: Movie


class LikedMovie(OrjsonConfigMixin):
    user: User
    movie: Movie
    score: int
