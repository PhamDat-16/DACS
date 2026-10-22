import uuid
from datetime import datetime
from typing import Optional, Union, Any

from pydantic import BaseModel, ConfigDict

from app.models.booking import BookingStatus


class BookingCreate(BaseModel):
    slot_id: Optional[uuid.UUID] = None
    slot_code: Optional[str] = None
    lot_id: Optional[Any] = None
    lot_name: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_hours: Optional[int] = 2
    vehicle_id: Optional[uuid.UUID] = None
    vehicle_plate: Optional[str] = None
    plate: Optional[str] = None


class BookingOut(BaseModel):
    id: uuid.UUID
    booking_id: Optional[str] = None
    code: Optional[str] = None
    slot_id: uuid.UUID
    slot_code: Optional[str] = None
    lot_name: Optional[str] = None
    vehicle_plate: Optional[str] = None
    plate: Optional[str] = None
    status: BookingStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    created_at: datetime
    qr_code: Optional[str] = None
    fee: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class BookingWithQR(BaseModel):
    booking: BookingOut
    qr_code_image: str  # base64 data-URI, frontend render trực tiếp bằng <img>
