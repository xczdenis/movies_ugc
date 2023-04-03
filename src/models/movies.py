from enum import Enum

from models.mixins import OrjsonConfigMixin, StrUUIDMixin
from models.users import User


class Movie(StrUUIDMixin, OrjsonConfigMixin):
    pass


class MoviePlaybackEventType(str, Enum):
    play = "play"
    pause = "pause"
    stop = "stop"
    fast_forward = "fast_forward"
    rewind = "rewind"


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
