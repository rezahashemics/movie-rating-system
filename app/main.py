from fastapi import FastAPI
from app.controllers.movie_controller import router as movie_router
from app.logging.logger import logger
from app.middlewares.logging_middleware import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router(movie_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")
