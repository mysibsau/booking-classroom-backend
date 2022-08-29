from typing import Optional

from pydantic import BaseModel, Field, UUID4
from schemas.equipment import EquipmentScheme
from schemas.common import BaseListRequestScheme, BaseListResponseScheme


class RoomScheme(BaseModel):
    id: UUID4 = Field(..., description="Room id")
    photo: str = Field(..., description="Path to photo")
    description: str = Field(..., description="description")
    address: str = Field(..., description="Address of room")
    capacity: int = Field(..., description="Capacity of room")
    equipment: list[EquipmentScheme]


class RoomFiltersScheme(BaseModel):
    address: Optional[str] = Field(None, description="Address of room")


class RoomListRequestScheme(BaseListRequestScheme):
    filters: Optional[RoomFiltersScheme] = Field(None, description="Filters")
    order_by: Optional[str] = Field("address")


class RoomListResponseScheme(BaseListResponseScheme):
    """Scenarios list response scheme.

    """

    data: list[RoomScheme] = Field(..., description="List of rooms")
