from abc import ABC
from typing import Any

from sqlalchemy import Select, func, MappingResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

class BaseRepository(ABC):
    """Base class for data repositories."""

    def __init__(self, read_session: AsyncSession, write_session: AsyncSession):
        self.read_session = read_session
        self.write_session = write_session

    async def _all(self, query: Select, read_only: bool = True):
        query = await self.read_session.scalars(query)\
            if read_only else await self.write_session.scalars(query)
        return query.all()

    async def _all_unique(self, query: Select, read_only: bool = True):
        result = await self.read_session.execute(query)\
            if read_only else await self.write_session.execute(query)
        return result.unique().scalars().all()

    async def _first(self, query: Select, read_only: bool = True):
        query = await self.read_session.scalars(query)\
            if read_only else await self.write_session.scalars(query)
        return query.first()

    async def _one_or_none(self, query: Select, read_only: bool = True):
        query = await self.read_session.scalars(query)\
            if read_only else await self.write_session.scalars(query)
        return query.one_or_none()

    async def _one(self, query: Select, read_only: bool = True):
        query = await self.read_session.scalars(query)\
            if read_only else await self.write_session.scalars(query)
        return query.one()

    async def _count(self, query: Select) -> int:
        query = query.subquery()
        query = await self.read_session.scalars(select(func.count()).select_from(query))
        return query.one()

    async def _raw(self, query: Any, read_only: bool = True):
        query = await self.read_session.execute(query)\
            if read_only else await self.write_session.execute(query)
        return MappingResult(query).all()
    
    async def _add(self, data: Any):
        self.write_session.add(data)
        await self.write_session.commit()
        await self.write_session.refresh(data)
        return data
    
    async def _update_commit(self, data: Any):
        await self.write_session.commit()
        return data

    async def _delete(self, data: Any):
        await self.write_session.delete(data)
        await self.write_session.commit()
        return data
    
    def _get_current_time(self):
        return func.now()