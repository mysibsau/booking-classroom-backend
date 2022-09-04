from uuid import uuid4

from .base import *


class BookingDateTime(Base):
    __tablename__ = "booking_date_time"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    booking_id = Column(UUID, ForeignKey("booking.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    booking = relationship("Booking", back_populates="booking_date_time", lazy='subquery')

    def __repr__(self):
        return f"{self.start_time} - {self.end_time}"
