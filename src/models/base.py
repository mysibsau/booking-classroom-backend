from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Float,
    Boolean,
    Table,
    ForeignKey,

)
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()
