from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_year = Column(Integer)
    description = Column(String)
