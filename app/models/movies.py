# app/models/movies.py (complete code with fix for cascade delete on ratings)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)
    release_year = Column(Integer, nullable=False)
    cast = Column(String)

    director = relationship("Director")
    genres = relationship("Genre", secondary="movie_genres", back_populates="movies")
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete")  # Fix: Add cascade delete for ratings
