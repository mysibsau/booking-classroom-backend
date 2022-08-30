from datetime import time, date

from pydantic import BaseModel, Field, UUID4

from schemas.enums.user_status_enum import UserStatusEnum


class BookingDateTimeScheme(BaseModel):
    booking_date: date = Field(...)
    start_time: time = Field(...)
    end_time: time = Field(...)


class CreateBookingScheme(BaseModel):
    user_id: str = Field(...)
    room_id: str = Field(...)
    contact_info: str = Field(...)
    description: str = Field(...)
    dates: list[BookingDateTimeScheme]
    booking_equipment: str = Field(...)
    user_status: UserStatusEnum = Field()
    position: str = Field()
