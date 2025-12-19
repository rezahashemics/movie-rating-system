from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.movies import Movie

db: Session = SessionLocal()
print(f"Movies count: {db.query(Movie).count()}")
db.close()
