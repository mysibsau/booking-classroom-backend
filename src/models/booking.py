from uuid import uuid4

from .base import *


class Booking(Base):
    __tablename__ = "booking"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    contact_info = Column(String(250), nullable=False)
    room_id = Column(UUID, ForeignKey("room.id"))
    description = Column(String(500), nullable=False)
    booking_date_time = relationship("BookingDateTime")
    booking_equipment = Column(String(500))
    user_status = Column(Enum(StatusEnum), default=StatusEnum.student)
    position = Column(String(100), nullable=False)
    status = Column(Enum(BookingStatusEnum), default=BookingStatusEnum.in_process)
    comment = Column(String(500), nullable=True)
    is_rejected = Column(Boolean, default=False)
    user = relationship("User", back_populates="booking", lazy='subquery')
    room = relationship("Room", back_populates="booking", lazy='subquery')
