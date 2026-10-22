from typing import Optional
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    username: Optional[str] = None
    phone: Optional[str] = None
    assigned_lot: Optional[str] = None
    shift: Optional[str] = "Ca Sáng (06h - 14h)"
    role: Optional[UserRole] = UserRole.customer


class StaffCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    username: str
    phone: Optional[str] = None
    assigned_lot: Optional[str] = None
    shift: Optional[str] = "Ca Sáng (06h - 14h)"


class UserLogin(BaseModel):
    email: str
    password: str


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    assigned_lot: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    shift: Optional[str] = "Ca Sáng (06h - 14h)"
    status: Optional[str] = "active"
    created_at: datetime

    # Cho phép Pydantic đọc trực tiếp từ SQLAlchemy model object (thay vì dict)
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    phone: str
    new_password: str

