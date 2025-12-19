from sqlalchemy import select
from app.models.movie_ratings import MovieRating
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
