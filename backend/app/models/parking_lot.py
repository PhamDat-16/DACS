import uuid

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ParkingLot(Base):
    __tablename__ = "parking_lots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    floor = Column(String(50), default="B1", nullable=True)
    address = Column(String(500), nullable=True)
    
    grid_width = Column(Integer, nullable=False)
    grid_height = Column(Integer, nullable=False)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    district = Column(String(100), nullable=True)
    city = Column(String(100), default="Hà Nội")
    hourly_base_rate = Column(Integer, default=25000)
    has_ev_charging = Column(Boolean, default=True)
    has_roof = Column(Boolean, default=True)
    status = Column(String(50), default="active")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    slots = relationship("ParkingSlot", back_populates="lot", cascade="all, delete-orphan")
    occupancy_logs = relationship("OccupancyHistory", back_populates="lot", cascade="all, delete-orphan")