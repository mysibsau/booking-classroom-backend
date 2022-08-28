from uuid import uuid4

from .base import *


class User(Base):
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100))
    status = Column(String(10), default="student")
    position = Column(String(100))
    role = Column(String(5), default="user")
