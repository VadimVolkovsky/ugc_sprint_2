from datetime import datetime
from uuid import UUID
from pydantic import Field, BaseModel
from models.films import LikeUser


class ReviewSchemaIn(BaseModel):
    text: str


class GradeSchemaIn(BaseModel):
    grade: int = Field(ge=0, le=1)


class ScoreSchemaOut(BaseModel):
    score: int


class ReviewFilmSchemaOut(BaseModel):
    id: UUID
    text: str
    created_at: datetime
    film_id: UUID
    likes: list[LikeUser]
