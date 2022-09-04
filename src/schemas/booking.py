from datetime import datetime

from pydantic import BaseModel, Field

from schemas.enums.user_status_enum import UserStatusEnum


class BookingDateTimeScheme(BaseModel):
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)


class CreateBookingScheme(BaseModel):
    user_id: str = Field(...)
    room_id: str = Field(...)
    contact_info: str = Field(...)
    description: str = Field(...)
    dates: list[BookingDateTimeScheme]
    booking_equipment: str = Field(...)
    user_status: UserStatusEnum = Field()
    position: str = Field()
