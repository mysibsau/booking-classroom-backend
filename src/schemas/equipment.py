from pydantic import BaseModel, Field


class EquipmentScheme(BaseModel):
    id: str = Field(...)
    name: str = Field(..., description="Name of equipment")
    description: str = Field(..., description="Description")
    count: int = Field(..., description="Count 0f equipment")
