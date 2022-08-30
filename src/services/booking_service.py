from services import PsqlService
from schemas.booking import CreateBookingScheme
from mappers.booking_mapper import create_booking_scheme_to_pg_data_mapper


class BookingService:

    __slots__ = '__psql_service'

    def __init__(self, psql_service: PsqlService):
        self.__psql_service = psql_service

    async def create_booking(self, request: CreateBookingScheme) -> None:
        await self.__psql_service.insert_one(create_booking_scheme_to_pg_data_mapper(request))
