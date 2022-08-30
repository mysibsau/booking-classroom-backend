from uuid import uuid4

from .base import *


class User(Base):
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    booking = relationship("Booking")

    def __repr__(self):
        return self.name