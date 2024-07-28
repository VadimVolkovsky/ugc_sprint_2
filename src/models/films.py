from datetime import datetime, timezone
from uuid import UUID, uuid4
from beanie import Document
from pydantic import Field, BaseModel


class Bookmark(BaseModel):
    id: UUID
    film_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LikeFilm(BaseModel):
    film_id: UUID
    grade: int


class LikeUser(BaseModel):
    user_id: UUID
    grade: int


class ReviewFilm(BaseModel):
    id: UUID
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    film_id: UUID
    likes: list[LikeUser]


class ReviewUser(BaseModel):
    id: UUID
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID
    likes: list[LikeUser]


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    likes: list[LikeFilm]
    reviews: list[ReviewFilm]
    bookmarks: list[Bookmark] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Film(Document):
    id: UUID = Field(default_factory=uuid4)
    likes: list[LikeUser]
    reviews: list[ReviewUser]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
