from pydantic import BaseModel, EmailStr
from app.core.settings import Status, StatusBook
from datetime import date

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class FoundSerial(BaseModel):
    id: int
    name: str
    premiered: date | None = None
    ended: date | None = None
    description: str
    season_amount: int
    poster: str | None = None
    imdb_rating: float | None = None
    status: Status

class FoundMovie(BaseModel):
    id: int
    name: str
    description: str
    year: int
    imdb_rating: float
    poster: str | None = None
    status: Status

class FoundBook(BaseModel):
    id: int
    author: str
    title: str
    description: str
    cover: str | None = None
    status: StatusBook

class AddSeries(BaseModel):
    tvmaze_id: str
    status: Status

class AddMovies(BaseModel):
    imdb_id: str
    status: Status

class AddBooks(BaseModel):
    olib_id: str
    author: str
    title: str
    cover: str
    status: StatusBook

class StatusFilter(BaseModel):
    status: Status

class StatusFilterBook(BaseModel):
    status: StatusBook