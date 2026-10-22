import uuid
import enum

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    slot_id = Column(UUID(as_uuid=True), ForeignKey("parking_slots.id"), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)

    qr_code = Column(String(255), unique=True, nullable=True)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.pending)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="bookings")
    slot = relationship("ParkingSlot", back_populates="bookings")
    vehicle = relationship("Vehicle", back_populates="bookings")
    session = relationship("ParkingSession", back_populates="booking", uselist=False)