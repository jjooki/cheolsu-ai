import logging

from fastapi import HTTPException, status
from functools import wraps
from openai import APIConnectionError, RateLimitError, APIStatusError

logger = logging.getLogger(__name__)

# Async decorator to handle exceptions about OpenAI API
def ahandle_openai_exception(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)  # 비동기 함수 처리

        except APIConnectionError as e:
            logging.error("The server could not be reached")
            logging.error(e.__cause__)  # an underlying Exception, likely raised within httpx.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_message=e.message,
            )
        
        except RateLimitError as e:
            error_message = "A 429 status code was received; we should back off a bit."
            logging.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                error_message=e.message,
            )
        
        except APIStatusError as e:
            logging.error(e.message)
            if e.status_code >= 500:
                error_message = "OpenAI Server Stop!"
                logging.critical(error_message)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.message,
                )
            
            else:
                error_message = "Another non-200-range status code was received"
                logging.error(error_message)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.message,
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while calling the openai chat.\n - Exception: {e}",
            )
        
        return result
    return wrapper

# Decorator to handle exceptions about OpenAI API
def handle_openai_exception(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

        except APIConnectionError as e:
            logging.error("The server could not be reached")
            logging.error(e.__cause__)  # an underlying Exception, likely raised within httpx.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_message=e.message,
            )
        
        except RateLimitError as e:
            error_message = "A 429 status code was received; we should back off a bit."
            logging.error(error_message)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                error_message=e.message,
            )
        
        except APIStatusError as e:
            logging.error(e.message)
            if e.status_code >= 500:
                error_message = "OpenAI Server Stop!"
                logging.critical(error_message)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.message,
                )
            
            else:
                error_message = "Another non-200-range status code was received"
                logging.error(error_message)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.message,
                )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while calling the openai chat.\n - Exception: {e}",
            )
        
        return result
    return wrapper