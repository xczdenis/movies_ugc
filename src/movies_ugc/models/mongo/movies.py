from beanie import Document
from config.types import TMovieId, TUserId
from pydantic import BaseModel, Field, conint


class UserMovieMixin(BaseModel):
    user_id: TUserId
    movie_id: TMovieId


class Like(Document):
    user_id: str
    movie_id: str
    score: conint(ge=0, le=10) = Field(..., description="Score between 0 and 10")

    class Settings:
        name = "likes"


class Favorite(Document, UserMovieMixin):
    class Settings:
        name = "favorites"
