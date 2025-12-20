# app/repositories/rating_repository.py (complete code with fix for NameError)
from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session
from app.models.movie_ratings import MovieRating
from app.models.movies import Movie  # Fix: Import Movie model
from app.exceptions.custom_exceptions import NotFoundException, ValidationException

class RatingRepository:
    def create_rating(self, db: Session, movie_id: int, score: int):
        # Check movie exists
        movie_query = select(Movie).filter(Movie.id == movie_id)
        if not db.scalar(movie_query):
            raise NotFoundException("Movie not found")

        if not 1 <= score <= 10:
            raise ValidationException("Score must be between 1 and 10")

        rating = MovieRating(movie_id=movie_id, score=score)
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating

    def get_average_rating(self, db: Session, movie_id: int):
        avg_query = select(func.avg(MovieRating.score)).filter(MovieRating.movie_id == movie_id)
        count_query = select(func.count(MovieRating.id)).filter(MovieRating.movie_id == movie_id)
        return db.scalar(avg_query), db.scalar(count_query)

    def delete_ratings_for_movie(self, db: Session, movie_id: int):
        db.execute(delete(MovieRating).where(MovieRating.movie_id == movie_id))
