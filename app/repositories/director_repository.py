# app/repositories/director_repository.py (complete code to fix ImportError)
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.directors import Director
from app.exceptions.custom_exceptions import ValidationException

class DirectorRepository:
    def get_director_by_id(self, db: Session, director_id: int):
        query = select(Director).filter(Director.id == director_id)
        director = db.scalar(query)
        if not director:
            raise ValidationException("Invalid director_id")
        return director
