from dependency_injector import containers, providers

from services import PsqlService, RoomService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    psql_service = providers.Singleton(PsqlService, connection_str=config.db_connection_string)
    room_service = providers.Factory(RoomService, psql_service)
