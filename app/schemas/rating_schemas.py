from pydantic import BaseModel, Field

class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=10)

class Rating(BaseModel):
    id: int
    movie_id: int
    score: int

    class Config:
        from_attributes = True
