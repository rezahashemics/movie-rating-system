from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request started: {request.method} {request.url.path}", extra={
            "route": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers)
        })
        try:
            response = await call_next(request)
            logger.info(f"Request completed: status_code={response.status_code}", extra={
                "route": request.url.path
            })
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}", extra={
                "route": request.url.path
            })
            raise
