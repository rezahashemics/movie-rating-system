from sqlalchemy.orm import Session
from app.repositories.rating_repository import RatingRepository
from app.schemas.rating_schemas import RatingCreate, Rating
from app.logging.logger import logger
from app.logging.decorators import log_function_call

class RatingService:
    def __init__(self):
        self.repo = RatingRepository()

    @log_function_call
    def create_rating(self, db: Session, movie_id: int, rating_data: RatingCreate):    
        try:
            if not 1 <= rating_data.score <= 10:
                logger.error("Invalid rating value", extra={
                    "movie_id": movie_id,
                    "rating": rating_data.score,
                    "route": f"/api/v1/movies/{movie_id}/ratings"
                })
                raise ValidationException("Score must be between 1 and 10")

            rating = self.repo.create_rating(db, movie_id, rating_data.score)
            logger.info("Rating saved successfully", extra={
                "movie_id": movie_id,
                "rating": rating_data.score,
                "route": f"/api/v1/movies/{movie_id}/ratings"
            })
            return Rating.from_orm(rating)
        except Exception as e:
            logger.error("Failed to save rating", extra={
                "movie_id": movie_id,
                "rating": rating_data.score,
                "error": str(e)
            })
            raise
