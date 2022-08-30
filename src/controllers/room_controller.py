from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from di_container import Container
from schemas.room import RoomListResponseScheme, RoomListRequestScheme
from services.room_service import RoomService

router = APIRouter(tags=["room"])


@router.post("/rooms/", response_model=RoomListResponseScheme)
@inject
async def get_rooms(request: RoomListRequestScheme, room_service: RoomService = Depends(Provide[Container.room_service])):

    return await room_service.search_room(request)
