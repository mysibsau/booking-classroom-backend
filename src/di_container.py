from dependency_injector import containers, providers

from services import PsqlService


class Container(containers.DeclarativeContainer):
    """DI Container

    """

    config = providers.Configuration()
    psql_service = providers.Singleton(PsqlService, connection_str=config.db_connection_string)
