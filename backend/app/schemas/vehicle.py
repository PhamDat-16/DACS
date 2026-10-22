import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from app.models.vehicle import VehicleType


class VehicleCreate(BaseModel):
    license_plate: str
    vehicle_type: VehicleType = VehicleType.car
    brand: Optional[str] = None
    color: Optional[str] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    user_id: Optional[uuid.UUID] = None


class VehicleUpdate(BaseModel):
    brand: Optional[str] = None
    color: Optional[str] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    vehicle_type: Optional[VehicleType] = None


class VehicleOut(BaseModel):
    id: uuid.UUID
    license_plate: str
    vehicle_type: VehicleType
    brand: Optional[str] = None
    color: Optional[str] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    check_in: Optional[str] = None
    check_in_date: Optional[str] = None
    assigned_lot: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
