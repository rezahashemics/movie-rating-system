from sqlalchemy import select, delete, func, and_
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.movies import Movie
from app.models.directors import Director
from app.models.genres import Genre
from app.models.movie_ratings import MovieRating
from app.exceptions.custom_exceptions import NotFoundException

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
