from typing import Any
from contextlib import asynccontextmanager

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from models import Base


class PsqlService:

    def __init__(self, connection_str: str):

        self.__engine = create_async_engine(connection_str)
        self.__async_session = sessionmaker(
            self.__engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def __session_scope(self) -> AsyncSession:

        session = self.__async_session()

        try:
            await session.begin()
            yield session
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise ex
        finally:
            await session.close()

    async def insert_one(self, data: Base) -> None:

        async with self.__session_scope() as session:
            session.add(data)
            await session.flush()

    async def insert_many(self, data: list[Base]) -> None:

        async with self.__session_scope() as session:
            session.add_all(data)
            await session.flush()

    async def execute(self, query: Any) -> ChunkedIteratorResult:

        async with self.__session_scope() as session:
            return await session.execute(query)

    async def get_count(self, query: Any, table: Base) -> int:

        count_query = query.with_only_columns([func.count()]).select_from(table).order_by(None)
        count = await self.execute(count_query)

        return count.scalar()
