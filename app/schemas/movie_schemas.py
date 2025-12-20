# app/schemas/movie_schemas.py (complete code with fix for cast required error - make all fields optional for update)
from pydantic import BaseModel, Field
from typing import List, Optional

class DirectorBase(BaseModel):
    name: str
    birth_year: Optional[int]
    description: Optional[str]

class Director(DirectorBase):
    id: int

class GenreBase(BaseModel):
    name: str
    description: Optional[str]

class Genre(GenreBase):
    id: int

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1)
    director_id: int
    release_year: int = Field(..., ge=1900, le=2100)
    cast: Optional[str] = None  # Optional for create if not required, but PDF example has it
    genres: List[int]  # List of genre IDs

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    release_year: Optional[int] = Field(None, ge=1900, le=2100)
    cast: Optional[str] = None  # Fix: Ensure optional with = None
    genres: Optional[List[int]] = None

class Movie(BaseModel):
    id: int
    title: str
    release_year: int
    director: Director
    genres: List[str]  # Names, not objects for response
    cast: Optional[str]
    average_rating: Optional[float]
    ratings_count: int

    class Config:
        from_attributes = True

class PaginatedMovies(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: List[Movie]
