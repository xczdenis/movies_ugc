from fastapi import APIRouter, Depends

from api.utils import make_rout_name
from api.v1.schemas.movies import (
    MoviePlaybackEventRequest,
    CurrentPlaybackPositionRequest,
    MovieViewingRequest,
)
from dependencies.interactors import get_movie_viewing_service
from internal.services.movie_viewing import MovieViewingService
from models.movies import MoviePlaybackEvent, Movie, CurrentPlaybackPosition, MovieViewing
from models.users import User

router = APIRouter(
    prefix="/movie",
)

NAMESPACE = "movie"


@router.post(
    "/add-playback-event",
    name=make_rout_name(NAMESPACE, "add_playback_event"),
    response_description="The event added successfully",
)
async def add_playback_event(
    request_event: MoviePlaybackEventRequest,
    service: MovieViewingService = Depends(get_movie_viewing_service),
) -> MoviePlaybackEvent:
    """
    Add data about an event that occurred while playing a movie
    """

    playback_event = MoviePlaybackEvent(
        user=User(id=request_event.user_id),
        movie=Movie(id=request_event.movie_id),
        event_type=request_event.event_type,
        playback_position=request_event.playback_position,
    )

    await service.add_playback_event(playback_event=playback_event)

    return playback_event


@router.post(
    "/add-movie-viewing",
    name=make_rout_name(NAMESPACE, "add_movie_viewing"),
    response_description="The movie viewing time added successfully",
)
async def add_movie_viewing(
    request_movie_viewing: MovieViewingRequest,
    service: MovieViewingService = Depends(get_movie_viewing_service),
) -> MovieViewing:
    """
    Add movie viewing time
    """

    movie_viewing = MovieViewing(
        user=User(id=request_movie_viewing.user_id),
        movie=Movie(id=request_movie_viewing.movie_id),
        viewed_seconds=request_movie_viewing.viewed_seconds,
    )

    await service.add_movie_viewing(movie_viewing=movie_viewing)

    return movie_viewing
