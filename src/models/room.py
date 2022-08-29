from uuid import uuid4

from .base import *


class Room(Base):
    __tablename__ = "room"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    photo = Column(String(100))
    description = Column(String(500))
    address = Column(String(100))
    capacity = Column(Integer)
    admin_id = Column(UUID, ForeignKey("user.id"))
    equipment = relationship("RoomEquipmentAssociation", back_populates="room", lazy='subquery', cascade="all, delete")

    def __repr__(self):
        return str(self.address)
