from fastapi import FastAPI
from sqladmin import Admin, ModelView
from models.user import User
from sqlalchemy.ext.asyncio import create_async_engine


class AdminApp:

    def __init__(self, app: FastAPI, connection_str: str):
        self.__app = app
        self.__engine = create_async_engine(connection_str)
        self.admin = Admin(self.__app, self.__engine)
        self.admin.add_view(UserAdmin)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.role, User.status, User.position]
