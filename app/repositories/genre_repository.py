# app/repositories/genre_repository.py (complete code to fix ImportError)
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.genres import Genre
from app.exceptions.custom_exceptions import ValidationException

class GenreRepository:
    def get_genres_by_ids(self, db: Session, genre_ids: list[int]):
        query = select(Genre).filter(Genre.id.in_(genre_ids))
        genres = db.scalars(query).all()
        if len(genres) != len(genre_ids):
            raise ValidationException("Invalid genres")
        return genres
