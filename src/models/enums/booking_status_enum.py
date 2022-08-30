from enum import Enum


class BookingStatusEnum(str, Enum):
    rejected = "отклонено"
    accepted = "одобрено"
    in_process = "В ожидании"
