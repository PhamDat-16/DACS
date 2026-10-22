import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.parking_slot import SlotStatus


class ParkingLotCreate(BaseModel):
    name: str
    address: Optional[str] = None
    grid_width: int
    grid_height: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district: Optional[str] = None
    city: Optional[str] = "Hà Nội"
    hourly_base_rate: Optional[int] = 25000
    has_ev_charging: Optional[bool] = True
    has_roof: Optional[bool] = True
    status: Optional[str] = "active"
    # Danh sách tọa độ (x, y) là chướng ngại vật - các ô còn lại tự động thành slot
    obstacle_positions: List[List[int]] = []


class ParkingSlotOut(BaseModel):
    id: uuid.UUID
    slot_code: str
    pos_x: int
    pos_y: int
    status: SlotStatus
    is_obstacle: bool

    model_config = ConfigDict(from_attributes=True)


class ParkingLotOut(BaseModel):
    id: uuid.UUID
    name: str
    address: Optional[str]
    grid_width: int
    grid_height: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district: Optional[str] = None
    city: Optional[str] = "Hà Nội"
    hourly_base_rate: Optional[int] = 25000
    has_ev_charging: Optional[bool] = True
    has_roof: Optional[bool] = True
    status: Optional[str] = "active"

    model_config = ConfigDict(from_attributes=True)


class ParkingLotDetail(ParkingLotOut):
    slots: List[ParkingSlotOut] = []


class CityLotNetworkOut(BaseModel):
    id: str
    name: str
    address: str
    district: str
    city: str
    latitude: float
    longitude: float
    grid_width: int
    grid_height: int
    total_slots: int
    available_slots: int
    occupancy_rate: float
    base_rate: int
    dynamic_rate: int
    tier: str
    tier_name: str
    has_ev: bool
    has_roof: bool
    status: str
    distance_km: Optional[float] = 1.0
    travel_time_min: Optional[int] = 5
