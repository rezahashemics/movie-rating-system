# app/logging/decorators.py (complete code with fix for KeyError)
import logging
import time
from functools import wraps
from app.logging.logger import logger  # Assume your JSON logger

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Function started: {func.__name__}", extra={
            "function_args": str(args),  # Fix: Renamed from 'args' to avoid reserved key conflict
            "kwargs": str(kwargs)
        })
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"Function completed successfully: {func.__name__}", extra={
                "duration": duration,
                "result": str(result)[:100]  # Truncate long results
            })
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Function failed: {func.__name__}", extra={
                "duration": duration,
                "error": str(e)
            })
            raise
    return wrapper
