# app/services/movie_service.py (complete code with fix for AttributeError)
from sqlalchemy.orm import Session
from app.repositories.movie_repository import MovieRepository
from app.repositories.rating_repository import RatingRepository
from app.schemas.movie_schemas import PaginatedMovies, Movie, MovieCreate, MovieUpdate, Director

class MovieService:
    def __init__(self):
        self.repo = MovieRepository()
        self.rating_repo = RatingRepository()

    def get_movies(self, db: Session, page: int = 1, page_size: int = 10, title: str = None, release_year: int = None, genre: str = None):
        movies, total = self.repo.get_movies(db, page, page_size, title, release_year, genre)
        movie_list = []
        for m in movies:
            avg, count = self.rating_repo.get_average_rating(db, m.id)
            # Fix: Create dict to avoid modifying ORM object; directly construct Pydantic model
            movie_data = {
                "id": m.id,
                "title": m.title,
                "release_year": m.release_year,
                "director": Director(
                    id=m.director.id,
                    name=m.director.name,
                    birth_year=m.director.birth_year,
                    description=m.director.description
                ),
                "genres": [g.name for g in m.genres],
                "cast": m.cast,
                "average_rating": avg,
                "ratings_count": count
            }
            movie_list.append(Movie(**movie_data))
        return PaginatedMovies(page=page, page_size=page_size, total_items=total, items=movie_list)

    def get_movie(self, db: Session, movie_id: int):
        movie = self.repo.get_movie_by_id(db, movie_id)
        avg, count = self.rating_repo.get_average_rating(db, movie.id)
        # Fix: Create dict to avoid modifying ORM object; directly construct Pydantic model
        movie_data = {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": Director(
                id=movie.director.id,
                name=movie.director.name,
                birth_year=movie.director.birth_year,
                description=movie.director.description
            ),
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": avg,
            "ratings_count": count
        }
        return Movie(**movie_data)

    def delete_movie(self, db: Session, movie_id: int):
        self.repo.delete_movie(db, movie_id)

    def create_movie(self, db: Session, movie_data: MovieCreate):
        movie = self.repo.create_movie(db, movie_data)
        avg, count = self.rating_repo.get_average_rating(db, movie.id)
        # Similar transformation for consistency
        movie_data_transformed = {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": Director(
                id=movie.director.id,
                name=movie.director.name,
                birth_year=movie.director.birth_year,
                description=movie.director.description
            ),
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": avg,
            "ratings_count": count
        }
        return Movie(**movie_data_transformed)

    def update_movie(self, db: Session, movie_id: int, movie_data: MovieUpdate):
        movie = self.repo.update_movie(db, movie_id, movie_data)
        avg, count = self.rating_repo.get_average_rating(db, movie.id)
        # Similar transformation for consistency
        movie_data_transformed = {
            "id": movie.id,
            "title": movie.title,
            "release_year": movie.release_year,
            "director": Director(
                id=movie.director.id,
                name=movie.director.name,
                birth_year=movie.director.birth_year,
                description=movie.director.description
            ),
            "genres": [g.name for g in movie.genres],
            "cast": movie.cast,
            "average_rating": avg,
            "ratings_count": count
        }
        return Movie(**movie_data_transformed)
