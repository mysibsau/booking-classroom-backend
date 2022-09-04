from schemas.booking import CreateBookingScheme
from models.booking import Booking
from uuid import uuid4

from mappers.datetime_mapper import booking_date_time_scheme_mapper_to_pg_data


def create_booking_scheme_to_pg_data_mapper(create_booking_scheme: CreateBookingScheme) -> Booking:
    booking_id = str(uuid4())
    return Booking(
        id=booking_id,
        user_id=create_booking_scheme.user_id,
        contact_info=create_booking_scheme.contact_info,
        room_id=create_booking_scheme.room_id,
        description=create_booking_scheme.description,
        user_status=create_booking_scheme.user_status,
        position=create_booking_scheme.position,
        booking_equipment=create_booking_scheme.booking_equipment,
        booking_date_time=[
            booking_date_time_scheme_mapper_to_pg_data(item, booking_id)
            for item in create_booking_scheme.dates
        ]
    )
