from enum import Enum


class UserStatusEnum(str, Enum):
    student = "student"
    staff = "staff"