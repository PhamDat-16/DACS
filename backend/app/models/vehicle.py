import uuid
import enum

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class VehicleType(str, enum.Enum):
    car = "car"
    motorcycle = "motorcycle"
    ev = "ev"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_plate = Column(String(50), unique=True, index=True, nullable=False)
    vehicle_type = Column(Enum(VehicleType), default=VehicleType.car, nullable=False)
    brand = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    owner_name = Column(String(255), nullable=True)
    owner_phone = Column(String(50), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    user = relationship("User", back_populates="vehicles")
    sessions = relationship("ParkingSession", back_populates="vehicle")
    bookings = relationship("Booking", back_populates="vehicle")