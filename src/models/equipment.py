from uuid import uuid4

from .base import *


class Equipment(Base):
    __tablename__ = "equipment"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500))
    room = relationship("RoomEquipmentAssociation", back_populates="equipment", cascade="all, delete")

    def __repr__(self):
        return self.name
