from typing import Any
from contextlib import asynccontextmanager

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from models import Base


class PsqlService:
    """Class for working with PostgreSQL.

    Methods
    -------
    `__session_scope(self) -> AsyncSession`
        Session scope manager.
    `insert_one(self, data: Base) -> None`
        Insert one object into DB.
    `insert_many(self, data: list[Base]) -> None`
        Insert more than one objects into DB.
    `execute(self, query: Any) -> ChunkedIteratorResult`
        Execute SQL query.
    `get_count(self, query: Any, table: Base) -> int`
        Get coutn of rows in DB table for SQL query.

    """

    def __init__(self, connection_str: str):
        """`PsqlService` class constructor.

        Parameters
        ----------
        `connection_str` : `str`
            Connetion string to PostgreSQL.

        """

        self.__engine = create_async_engine(connection_str)
        self.__async_session = sessionmaker(
            self.__engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def __session_scope(self) -> AsyncSession:
        """Session scope manager.

        Return
        ------
        `AsyncSession`
            Async session.

        """

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
        """Insert one object into DB.

        Parameters
        ----------
        `data` : `Base`
            SQLAlchemy model.

        """

        async with self.__session_scope() as session:
            session.add(data)
            await session.flush()

    async def insert_many(self, data: list[Base]) -> None:
        """Insert more then one objects into DB.

        Parameters
        ----------
        `data` : `Base`
            SQLAlchemy model.

        """

        async with self.__session_scope() as session:
            session.add_all(data)
            await session.flush()

    async def execute(self, query: Any) -> ChunkedIteratorResult:
        """Execute SQL query.

        Parameters
        ----------
        `query` : `Any`
            SQL query.

        Return
        ------
        `ChunkedIteratorResult`
            Result of query execution.

        """

        async with self.__session_scope() as session:
            return await session.execute(query)

    async def get_count(self, query: Any, table: Base) -> int:
        """Get coutn of rows in DB table for SQL query.

        Parameters
        ----------
        `query` : `Any`
            SQL query.
        `table` : `Base`
            Table for counting.

        Return
        ------
        `int`
            Count of rows in DB table for query.

        """

        count_query = query.with_only_columns([func.count()]).select_from(table).order_by(None)
        count = await self.execute(count_query)

        return count.scalar()
