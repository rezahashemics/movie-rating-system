# app/repositories/movie_repository.py (complete code with all fixes)
from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.movies import Movie
from app.models.genres import Genre
from app.models.directors import Director
from app.models.movie_ratings import MovieRating
from app.models.movie_genres import movie_genres
from app.repositories.director_repository import DirectorRepository
from app.repositories.genre_repository import GenreRepository
from app.exceptions.custom_exceptions import NotFoundException, ValidationException

class MovieRepository:
    def get_movies(self, db: Session, page: int, page_size: int, title: str = None, release_year: int = None, genre: str = None):
        query = select(Movie).options(
            joinedload(Movie.director),
            selectinload(Movie.genres)
        )

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        if genre:
            query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre}%"))

        total = db.scalar(select(func.count()).select_from(query.subquery()))
        movies = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()

        return movies, total

    def get_movie_by_id(self, db: Session, movie_id: int):
        query = select(Movie).filter(Movie.id == movie_id).options(
            joinedload(Movie.director),
            selectinload(Movie.genres)
        )
        movie = db.scalar(query)
        if not movie:
            raise NotFoundException("Movie not found")
        return movie

    def delete_movie(self, db: Session, movie_id: int):
        movie = self.get_movie_by_id(db, movie_id)  # Raises if not found
        db.delete(movie)
        db.commit()

    def create_movie(self, db: Session, movie_data):
        dir_repo = DirectorRepository()
        dir_repo.get_director_by_id(db, movie_data.director_id)  # Validates

        genre_repo = GenreRepository()
        genre_repo.get_genres_by_ids(db, movie_data.genres)  # Validates

        movie = Movie(
            title=movie_data.title,
            director_id=movie_data.director_id,
            release_year=movie_data.release_year,
            cast=movie_data.cast
        )
        db.add(movie)
        db.flush()

        # Add genres
        for genre_id in movie_data.genres:
            db.execute(movie_genres.insert().values(movie_id=movie.id, genre_id=genre_id))

        db.commit()
        db.refresh(movie)
        return movie

    def update_movie(self, db: Session, movie_id: int, movie_data):
        movie = self.get_movie_by_id(db, movie_id)  # Raises if not found

        if movie_data.title is not None:
            movie.title = movie_data.title
        if movie_data.release_year is not None:
            movie.release_year = movie_data.release_year
        if movie_data.cast is not None:
            movie.cast = movie_data.cast

        if movie_data.genres is not None:
            # Clear existing genres
            db.execute(delete(movie_genres).where(movie_genres.c.movie_id == movie_id))
            genre_repo = GenreRepository()
            genre_repo.get_genres_by_ids(db, movie_data.genres)  # Validates
            # Add new
            for genre_id in movie_data.genres:
                db.execute(movie_genres.insert().values(movie_id=movie_id, genre_id=genre_id))

        db.commit()
        db.refresh(movie)
        return movie
