from abc import ABC
from typing import Any

from sqlalchemy import Select, func, Text, MappingResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select


class BaseRepository(ABC):
    """Base class for data repositories."""

    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def _all(self, query: Select):
        query = await self.session.scalars(query)
        return query.all()

    async def _all_unique(self, query: Select):
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def _first(self, query: Select):
        query = await self.session.scalars(query)
        return query.first()

    async def _one_or_none(self, query: Select):
        query = await self.session.scalars(query)
        return query.one_or_none()

    async def _one(self, query: Select):
        query = await self.session.scalars(query)
        return query.one()

    async def _count(self, query: Select) -> int:
        query = query.subquery()
        query = await self.session.scalars(select(func.count()).select_from(query))
        return query.one()

    async def _raw(self, query: Any):
        query = await self.session.execute(query)
        return MappingResult(query).all()
