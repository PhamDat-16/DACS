import uuid
import enum

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SessionStatus(str, enum.Enum):
    PARKING = "PARKING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    parking = "PARKING"
    completed = "COMPLETED"
    cancelled = "CANCELLED"


class ParkingSession(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=True)
    slot_id = Column(UUID(as_uuid=True), ForeignKey("parking_slots.id"), nullable=False)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=True)

    check_in_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    check_out_time = Column(DateTime(timezone=True), nullable=True)

    check_in_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    check_out_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    handled_by_staff = Column(String(255), nullable=True)

    status = Column(Enum(SessionStatus), nullable=False, default=SessionStatus.PARKING)
    total_fee = Column(Integer, default=0, nullable=True)
    note = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    vehicle = relationship("Vehicle", back_populates="sessions")
    slot = relationship("ParkingSlot", back_populates="sessions")
    booking = relationship("Booking", back_populates="session")
    check_in_staff = relationship(
        "User",
        foreign_keys=[check_in_by],
        back_populates="checked_in_sessions",
    )
    check_out_staff = relationship(
        "User",
        foreign_keys=[check_out_by],
        back_populates="checked_out_sessions",
    )

    @property
    def slot_code(self):
        return self.slot.slot_code if self.slot else None

    @property
    def lot_name(self):
        if self.slot and self.slot.lot:
            return self.slot.lot.name
        return None

    @property
    def license_plate(self):
        if self.vehicle:
            return self.vehicle.license_plate
        if self.booking and self.booking.vehicle:
            return self.booking.vehicle.license_plate
        return None