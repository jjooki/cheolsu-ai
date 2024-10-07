import asyncio
import logging

from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.common.config import config

database_url = (
    f"mysql+aiomysql://{config.DATABASE.USERNAMES}:{config.DATABASE.PASSWORD}"
    f"@{config.DATABASE.HOST}/{config.DATABASE.DATABASE}"
)
read_database_url = (
    f"mysql+aiomysql://{config.DATABASE.USERNAMES}:{config.DATABASE.PASSWORD}"
    f"@{config.DATABASE.RO_HOST}/{config.DATABASE.DATABASE}"
)

session_context: ContextVar[str] = ContextVar("session_context")

# Use connection pooling with optimized settings
base_engine = create_async_engine(
    url=database_url,
    echo=True,
    # pool_size=30,  # Increase pool size
    # max_overflow=50,  # Increase max overflow
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=36000,
)
# Use connection pooling with optimized settings
read_engine = create_async_engine(
    url=read_database_url,
    echo=True,
    # pool_size=30,  # Increase pool size
    # max_overflow=50,  # Increase max overflow
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=36000,
)

async_session = async_sessionmaker(base_engine, expire_on_commit=False)
async_read_session = async_sessionmaker(read_engine, expire_on_commit=False)

# Define a semaphore to limit the number of concurrent sessions
sem = asyncio.Semaphore(30)  # Adjust the limit based on your requirements

# Uncomment asynccontextmanager for test
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sem:
        session = async_session()
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            logger.error("Database error occurred: %s", e)
            await session.rollback()
            raise
        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.info("Session closed")

# Uncomment asynccontextmanager for test
@asynccontextmanager
async def get_read_session() -> AsyncGenerator[AsyncSession, None]:
    async with sem:
        session = async_read_session()
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            logger.error("Database error occurred: %s", e)
            await session.rollback()
            raise
        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.info("Session closed")

Base = declarative_base()