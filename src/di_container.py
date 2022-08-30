from dependency_injector import containers, providers

from services import PsqlService, RoomService, BookingService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    psql_service = providers.Singleton(PsqlService, connection_str=config.db_connection_string)
    room_service = providers.Factory(RoomService, psql_service=psql_service)
    booking_service = providers.Factory(BookingService, psql_service=psql_service)
