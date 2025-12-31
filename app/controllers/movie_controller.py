from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.movie_service import MovieService
from app.services.rating_service import RatingService
from app.schemas.movie_schemas import MovieCreate, MovieUpdate, Movie
from app.schemas.rating_schemas import RatingCreate

router = APIRouter()

# --- Dependency Providers ---

def get_movie_service() -> MovieService:
    """Provider for MovieService instance."""
    return MovieService()

def get_rating_service() -> RatingService:
    """Provider for RatingService instance."""
    return RatingService()

# --- Routes ---

@router.get("/movies", response_model=dict)
def get_movies(
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, ge=1, le=100),
    title: str = None, 
    release_year: int = None, 
    genre: str = None,
    db: Session = Depends(get_db),
    movie_service: MovieService = Depends(get_movie_service)
):
    data = movie_service.get_movies(db, page, page_size, title, release_year, genre)
    return {"status": "success", "data": data.dict()}

@router.get("/movies/{movie_id}", response_model=dict)
def get_movie(
    movie_id: int, 
    db: Session = Depends(get_db),
    movie_service: MovieService = Depends(get_movie_service)
):
    data = movie_service.get_movie(db, movie_id)
    return {"status": "success", "data": data.dict()}

@router.post("/movies", response_model=dict, status_code=201)
def create_movie(
    movie: MovieCreate, 
    db: Session = Depends(get_db),
    movie_service: MovieService = Depends(get_movie_service)
):
    data = movie_service.create_movie(db, movie)
    return {"status": "success", "data": data.dict()}

@router.put("/movies/{movie_id}", response_model=dict)
def update_movie(
    movie_id: int, 
    movie: MovieUpdate, 
    db: Session = Depends(get_db),
    movie_service: MovieService = Depends(get_movie_service)
):
    data = movie_service.update_movie(db, movie_id, movie)
    return {"status": "success", "data": data.dict()}

@router.delete("/movies/{movie_id}", status_code=204)
def delete_movie(
    movie_id: int, 
    db: Session = Depends(get_db),
    movie_service: MovieService = Depends(get_movie_service)
):
    movie_service.delete_movie(db, movie_id)
    return None

@router.post("/movies/{movie_id}/ratings", response_model=dict, status_code=201)
def create_rating(
    movie_id: int, 
    rating: RatingCreate, 
    db: Session = Depends(get_db),
    rating_service: RatingService = Depends(get_rating_service)
):
    data = rating_service.create_rating(db, movie_id, rating)
    return {"status": "success", "data": data.dict()}
