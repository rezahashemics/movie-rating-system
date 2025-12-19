from sqlalchemy import select, delete, func, and_
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.movies import Movie
from app.models.directors import Director
from app.models.genres import Genre
from app.models.movie_ratings import MovieRating
from app.exceptions.custom_exceptions import NotFoundException
from app.exceptions.custom_exceptions import ValidationException

class MovieRepository:
    def create_movie(self, db: Session, movie_data):
        # Validate director
        dir_query = select(Director).filter(Director.id == movie_data.director_id)
        if not db.scalar(dir_query):
            raise ValidationException("Invalid director_id")

      # Validate genres
        genres_query = select(Genre).filter(Genre.id.in_(movie_data.genres))
        valid_genres = db.scalars(genres_query).all()
        if len(valid_genres) != len(movie_data.genres):
            raise ValidationException("Invalid genres")

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
        return self.get_movie_by_id(db, movie.id)  # Reuse Reza's method

    def update_movie(self, db: Session, movie_id: int, movie_data):
        movie = self.get_movie_by_id(db, movie_id)  # Raises if not found

        if movie_data.title:
            movie.title = movie_data.title
        if movie_data.release_year:
            movie.release_year = movie_data.release_year
        if movie_data.cast:
            movie.cast = movie_data.cast

        if movie_data.genres is not None:
            # Clear existing genres
            db.execute(delete(movie_genres).where(movie_genres.c.movie_id == movie_id))
            # Add new
            for genre_id in movie_data.genres:
                genre_query = select(Genre).filter(Genre.id == genre_id)
                if not db.scalar(genre_query):
                    raise ValidationException("Invalid genre_id")
                db.execute(movie_genres.insert().values(movie_id=movie_id, genre_id=genre_id))

        db.commit()
        db.refresh(movie)
        return movie
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

        for movie in movies:
            avg_query = select(func.avg(MovieRating.score)).filter(MovieRating.movie_id == movie.id)
            movie.average_rating = db.scalar(avg_query)
            movie.ratings_count = db.scalar(select(func.count(MovieRating.id)).filter(MovieRating.movie_id == movie.id))

        return movies, total

    def get_movie_by_id(self, db: Session, movie_id: int):
        query = select(Movie).filter(Movie.id == movie_id).options(
            joinedload(Movie.director),
            selectinload(Movie.genres)
        )
        movie = db.scalar(query)
        if not movie:
            raise NotFoundException("Movie not found")
        avg_query = select(func.avg(MovieRating.score)).filter(MovieRating.movie_id == movie.id)
        movie.average_rating = db.scalar(avg_query)
        movie.ratings_count = db.scalar(select(func.count(MovieRating.id)).filter(MovieRating.movie_id == movie.id))
        return movie

    def delete_movie(self, db: Session, movie_id: int):
        movie = self.get_movie_by_id(db, movie_id)  # Raises if not found
        db.delete(movie)
        db.commit()
