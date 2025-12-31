import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.movies import Movie

db: Session = SessionLocal()
print(f"Movies count: {db.query(Movie).count()}")
db.close()
