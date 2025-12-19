from sqlalchemy.orm import Session
from app.repositories.movie_repository import MovieRepository
from app.schemas.movie_schemas import PaginatedMovies, Movie, MovieCreate, MovieUpdate

class MovieService:
    def __init__(self):
        self.repo = MovieRepository()

    def get_movies(self, db: Session, page: int = 1, page_size: int = 10, title: str = None, release_year: int = None, genre: str = None):
        movies, total = self.repo.get_movies(db, page, page_size, title, release_year, genre)
        return PaginatedMovies(page=page, page_size=page_size, total_items=total, items=[Movie.from_orm(m) for m in movies])

    def get_movie(self, db: Session, movie_id: int):
        movie = self.repo.get_movie_by_id(db, movie_id)
        return Movie.from_orm(movie)

    def delete_movie(self, db: Session, movie_id: int):
        self.repo.delete_movie(db, movie_id)
    def create_movie(self, db: Session, movie_data: MovieCreate):
        movie = self.repo.create_movie(db, movie_data)
        return Movie.from_orm(movie)

    def update_movie(self, db: Session, movie_id: int, movie_data: MovieUpdate):
        movie = self.repo.update_movie(db, movie_id, movie_data)
        return Movie.from_orm(movie)
