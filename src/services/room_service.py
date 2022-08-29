from sqlalchemy.future import select
from services import PsqlService

from models.room import Room
from mappers.room_mapper import pg_data_to_room_scheme_mapper
from schemas.room import RoomListRequestScheme, RoomListResponseScheme


class RoomService:

    __slots__ = '__psql_service'

    def __init__(self, psql_service: PsqlService):
        self.__psql_service = psql_service

    async def search_playlist(self, request: RoomListRequestScheme) -> RoomListResponseScheme:

        search_query = select(Room)

        if request.filters.address:
            search_query = search_query.where(Room.address.like(f'%{request.filters.address}%'))

        order_desc = request.order_desc
        order_by = getattr(Room, request.order_by)
        count = await self.__psql_service.get_count(search_query, Room)
        search_query = (
            search_query
            .order_by(order_by.desc() if order_desc else order_by.asc())
            .offset((request.page - 1) * request.per_page)
            .limit(request.per_page)
        )

        result = await self.__psql_service.execute(search_query)

        return RoomListResponseScheme(
            data=[
                pg_data_to_room_scheme_mapper(room)
                for room in result.scalars().all()
            ],
            page=request.page,
            per_page=request.per_page,
            count=count
        )
