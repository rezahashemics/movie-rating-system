# app/models/movie_ratings.py (complete code with fix for IntegrityError)
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class MovieRating(Base):
    __tablename__ = "movie_ratings"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)  # Fix: Add ondelete="CASCADE" for auto-delete ratings on movie delete
    score = Column(Integer, nullable=False)

    movie = relationship("Movie", back_populates="ratings")
