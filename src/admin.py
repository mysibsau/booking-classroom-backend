from fastapi import FastAPI
from sqladmin import Admin, ModelView
from models.user import User
from models.room import Room
from models.equipment import Equipment
from models.room_equipment_association import RoomEquipmentAssociation
from sqlalchemy.ext.asyncio import create_async_engine


class AdminApp:

    def __init__(self, app: FastAPI, connection_str: str):
        self.__app = app
        self.__engine = create_async_engine(connection_str)
        self.admin = Admin(self.__app, self.__engine)
        self.admin.add_view(UserAdmin)
        self.admin.add_view(RoomAdmin)
        self.admin.add_view(EquipmentAdmin)
        self.admin.add_view(EquipmentInRoomAdmin)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.role, User.status, User.position]


class RoomAdmin(ModelView, model=Room):
    column_list = [Room.address, Room.equipment]


class EquipmentAdmin(ModelView, model=Equipment):
    column_list = [Equipment.name, Equipment.description]


class EquipmentInRoomAdmin(ModelView, model=RoomEquipmentAssociation):
    column_list = [
        RoomEquipmentAssociation.room,
        RoomEquipmentAssociation.equipment,
        RoomEquipmentAssociation.count,
        ]
