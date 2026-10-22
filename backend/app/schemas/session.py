import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CheckInRequest(BaseModel):
    qr_code: Optional[str] = None  # token quét được từ mã QR của khách
    license_plate: Optional[str] = None  # Biển số xe quét qua camera / nhập bốt
    plate: Optional[str] = None
    slot_id: Optional[uuid.UUID] = None
    slot_code: Optional[str] = None
    lot_name: Optional[str] = None


class CheckOutRequest(BaseModel):
    session_id: Optional[uuid.UUID] = None
    license_plate: Optional[str] = None
    plate: Optional[str] = None
    slot_code: Optional[str] = None


class SessionOut(BaseModel):
    id: uuid.UUID
    slot_id: uuid.UUID
    booking_id: Optional[uuid.UUID] = None
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    handled_by_staff: Optional[str] = None
    total_fee: Optional[int] = 0
    note: Optional[str] = None
    license_plate: Optional[str] = None
    slot_code: Optional[str] = None
    lot_name: Optional[str] = None
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

