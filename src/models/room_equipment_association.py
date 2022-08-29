from uuid import uuid4

from .base import *


class RoomEquipmentAssociation(Base):
    __tablename__ = "room_equipment_association"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    room_id = Column(ForeignKey("room.id"), nullable=False)
    equipment_id = Column(ForeignKey("equipment.id"), nullable=False)
    count = Column(Integer, nullable=False)
    room = relationship("Room", back_populates="equipment")
    equipment = relationship("Equipment", back_populates="room", lazy='subquery')

    def __repr__(self):
        return f"{self.equipment.name}: {self.count}"
