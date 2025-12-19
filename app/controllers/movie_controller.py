from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.movie_service import MovieService
from app.schemas.movie_schemas import PaginatedMovies, Movie

router = APIRouter()

@router.get("/movies", response_model=dict)
def get_movies(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100),
               title: str = None, release_year: int = None, genre: str = None,
               db: Session = Depends(get_db)):
    service = MovieService()
    data = service.get_movies(db, page, page_size, title, release_year, genre)
    return {"status": "success", "data": data.dict()}

@router.get("/movies/{movie_id}", response_model=dict)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService()
    data = service.get_movie(db, movie_id)
    return {"status": "success", "data": data.dict()}

@router.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    service = MovieService()
    service.delete_movie(db, movie_id)
    return None
