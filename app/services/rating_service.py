from sqlalchemy.orm import Session
from app.repositories.rating_repository import RatingRepository
from app.schemas.rating_schemas import RatingCreate, Rating

class RatingService:
    def __init__(self):
        self.repo = RatingRepository()

    def create_rating(self, db: Session, movie_id: int, rating_data: RatingCreate):
        rating = self.repo.create_rating(db, movie_id, rating_data.score)
        return Rating.from_orm(rating)
