import uuid
import enum

from sqlalchemy import Column, String, Integer, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class SlotStatus(str, enum.Enum):
    available = "available"
    reserved = "reserved"
    occupied = "occupied"
    maintenance = "maintenance"


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lot_id = Column(UUID(as_uuid=True), ForeignKey("parking_lots.id"), nullable=False)
    slot_code = Column(String(50), nullable=False)
    vehicle_type = Column(String(50), default="car", nullable=False)

    pos_x = Column(Integer, nullable=False)
    pos_y = Column(Integer, nullable=False)

    status = Column(Enum(SlotStatus), nullable=False, default=SlotStatus.available)
    is_obstacle = Column(Boolean, nullable=False, default=False)

    lot = relationship("ParkingLot", back_populates="slots")
    bookings = relationship("Booking", back_populates="slot")
    sessions = relationship("ParkingSession", back_populates="slot")