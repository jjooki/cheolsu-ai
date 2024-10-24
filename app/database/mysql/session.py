import asyncio
import logging

from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, DeclarativeMeta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.common.config import config

base_database_url = URL.create(
    drivername="mysql+pymysql",
    username=config.DATABASE.USERNAMES,
    password=config.DATABASE.PASSWORD,
    port=config.DATABASE.DB_PORT,
    host=config.DATABASE.HOST,
    database=config.DATABASE.DATABASE,
)

database_url = URL.create(
    drivername="mysql+aiomysql",
    username=config.DATABASE.USERNAMES,
    password=config.DATABASE.PASSWORD,
    host=config.DATABASE.HOST,
    database=config.DATABASE.DATABASE,
    port=config.DATABASE.DB_PORT,
)

read_database_url = URL.create(
    drivername="mysql+aiomysql",
    username=config.DATABASE.USERNAMES,
    password=config.DATABASE.PASSWORD,
    host=config.DATABASE.RO_HOST,
    database=config.DATABASE.DATABASE,
    port=config.DATABASE.DB_PORT,
)

session_context: ContextVar[str] = ContextVar("session_context")

# Use connection pooling with optimized settings
base_engine = create_engine(
    url=base_database_url, connect_args={}
)
write_engine = create_async_engine(
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

async_session = async_sessionmaker(write_engine, expire_on_commit=False)
async_read_session = async_sessionmaker(read_engine, expire_on_commit=False)

# Define a semaphore to limit the number of concurrent sessions
sem = asyncio.Semaphore(30)  # Adjust the limit based on your requirements

# Uncomment asynccontextmanager for test
# @asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sem:
        session = async_session()
        try:
            yield session
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
# @asynccontextmanager
async def get_read_session() -> AsyncGenerator[AsyncSession, None]:
    async with sem:
        session = async_read_session()
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error("Database error occurred: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error occurred: %s", e)
            raise
        finally:
            await session.close()
            logger.info("Session closed")

Base: DeclarativeMeta = declarative_base()