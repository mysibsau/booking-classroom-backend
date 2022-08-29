from typing import Optional

from pydantic import BaseModel, Field


class BaseListRequestScheme(BaseModel):
    """Base list request scheme.

    """

    page: Optional[int] = Field(1, description="Current page")
    per_page: Optional[int] = Field(10, description="Elements per page")
    order_desc: Optional[bool] = Field(True, description="Order desc or not")


class BaseListResponseScheme(BaseModel):
    """Base list response scheme.

    """

    page: int = Field(..., description="Current page")
    per_page: int = Field(..., description="Elements per page")
    count: int = Field(..., description="Count of all elements")


