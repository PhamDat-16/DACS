import uuid
import enum

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UserRole(str, enum.Enum):
    customer = "customer"
    staff = "staff"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.customer)
    assigned_lot = Column(String(255), nullable=True, default=None)
    status = Column(String(50), nullable=False, default="active")
    shift = Column(String(100), nullable=True, default="Ca Sáng (06h - 14h)")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    bookings = relationship("Booking", back_populates="user")
    vehicles = relationship("Vehicle", back_populates="user")
    checked_in_sessions = relationship(
        "ParkingSession",
        foreign_keys="ParkingSession.check_in_by",
        back_populates="check_in_staff",
    )
    checked_out_sessions = relationship(
        "ParkingSession",
        foreign_keys="ParkingSession.check_out_by",
        back_populates="check_out_staff",
    )