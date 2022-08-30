from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from di_container import Container
from schemas.booking import CreateBookingScheme
from services.booking_service import BookingService

router = APIRouter(tags=["booking"])


@router.post("/booking/create")
@inject
async def get_rooms(request: CreateBookingScheme, booking_service: BookingService = Depends(Provide[Container.booking_service])):

    return await booking_service.create_booking(request)

