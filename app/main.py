from fastapi import FastAPI
from app.controllers.movie_controller import router as movie_router

app = FastAPI()

app.include_router(movie_router, prefix="/api/v1")
