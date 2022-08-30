from models.booking_datetime import BookingDateTime
from schemas.booking import BookingDateTimeScheme


def booking_date_time_scheme_mapper_to_pg_data(request: BookingDateTimeScheme, booking_id: str) -> BookingDateTime:
    return BookingDateTime(
        booking_id=booking_id,
        date=request.booking_date,
        start_time=request.start_time,
        end_time=request.end_time,
    )
