from typing import List
import uuid
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.schemas.user import UserOut, StaffCreate, ProfileUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


class UpdateStatusPayload(BaseModel):
    status: str


class UpdatePasswordPayload(BaseModel):
    new_password: str


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Endpoint đơn giản để test luồng JWT đầu-cuối: login -> lấy token -> gọi /me."""
    return current_user


@router.put("/me", response_model=UserOut)
def update_current_user(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: DbSession = Depends(get_db),
):
    """
    Cập nhật thông tin tài khoản (full_name, phone, email) của người dùng hiện tại
    và lưu trực tiếp vào cơ sở dữ liệu PostgreSQL.
    """
    if payload.email:
        clean_email = payload.email.strip().lower()
        if clean_email != current_user.email.lower():
            existing = (
                db.query(User)
                .filter(User.email.ilike(clean_email), User.id != current_user.id)
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{clean_email}' đã được đăng ký bởi tài khoản khác trong hệ thống!",
                )
            current_user.email = clean_email

    if payload.full_name is not None:
        clean_name = payload.full_name.strip()
        if clean_name:
            current_user.full_name = clean_name

    if payload.phone is not None:
        clean_phone = payload.phone.strip()
        current_user.phone = clean_phone if clean_phone else None

    db.commit()
    db.refresh(current_user)
    return current_user


@router.put("/{user_id}/profile", response_model=UserOut)
def update_user_profile(
    user_id: uuid.UUID,
    payload: ProfileUpdate,
    db: DbSession = Depends(get_db),
):
    """
    Cập nhật thông tin người dùng theo user_id lưu vào database PostgreSQL.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy tài khoản người dùng!",
        )

    if payload.email:
        clean_email = payload.email.strip().lower()
        if clean_email != user.email.lower():
            existing = (
                db.query(User)
                .filter(User.email.ilike(clean_email), User.id != user.id)
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email '{clean_email}' đã được đăng ký bởi tài khoản khác!",
                )
            user.email = clean_email

    if payload.full_name is not None:
        clean_name = payload.full_name.strip()
        if clean_name:
            user.full_name = clean_name

    if payload.phone is not None:
        clean_phone = payload.phone.strip()
        user.phone = clean_phone if clean_phone else None

    db.commit()
    db.refresh(user)
    return user


@router.get("/staff", response_model=List[UserOut])
def get_staff_users(db: DbSession = Depends(get_db)):
    """Lấy danh sách tất cả nhân viên bảo vệ và quản trị viên từ database."""
    staff_members = (
        db.query(User)
        .filter(User.role.in_([UserRole.staff, UserRole.admin]))
        .order_by(User.created_at.asc())
        .all()
    )
    return staff_members


@router.post("/staff", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_staff_user(payload: StaffCreate, db: DbSession = Depends(get_db)):
    """Admin tạo tài khoản nhân viên mới lưu trực tiếp vào cơ sở dữ liệu PostgreSQL."""
    clean_email = payload.email.strip().lower()
    clean_username = payload.username.strip().lower()

    if db.query(User).filter(User.email.ilike(clean_email)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{clean_email}' đã được đăng ký trong hệ thống!",
        )

    if db.query(User).filter(User.username.ilike(clean_username)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tên đăng nhập (username) '{clean_username}' đã tồn tại!",
        )

    assigned_lot_name = (payload.assigned_lot or "").strip()

    # Tự động đồng bộ và tạo mới Bãi đỗ xe vào Database nếu chưa tồn tại
    if assigned_lot_name and "Toàn Hệ Thống" not in assigned_lot_name:
        existing_lot = db.query(ParkingLot).filter(ParkingLot.name.ilike(assigned_lot_name)).first()
        if not existing_lot:
            new_lot = ParkingLot(
                name=assigned_lot_name,
                address=f"Khu vực {assigned_lot_name}, Hà Nội",
                district="Hà Nội",
                city="Hà Nội",
                grid_width=5,
                grid_height=4,
                hourly_base_rate=15000,
                has_ev_charging=True,
                has_roof=True,
                status="active"
            )
            db.add(new_lot)
            db.flush()
            # Sinh 10 slot mẫu cho bãi này (A-001 đến A-010)
            slots_to_add = [
                ParkingSlot(
                    lot_id=new_lot.id,
                    slot_code=f"A-{i:03d}",
                    vehicle_type="car" if i <= 7 else "motorcycle",
                    pos_x=i - 1,
                    pos_y=0,
                    status=SlotStatus.available
                ) for i in range(1, 11)
            ]
            db.add_all(slots_to_add)
            db.flush()

    new_user = User(
        email=clean_email,
        username=clean_username,
        full_name=payload.full_name.strip(),
        phone=payload.phone.strip() if payload.phone else None,
        assigned_lot=assigned_lot_name,
        shift=payload.shift or "Ca Sáng (06h - 14h)",
        password_hash=hash_password(payload.password),
        role=UserRole.staff,
        status="active",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}/status", response_model=UserOut)
def update_user_status(
    user_id: uuid.UUID,
    payload: UpdateStatusPayload,
    db: DbSession = Depends(get_db),
):
    """Cập nhật trạng thái khóa/mở khóa tài khoản."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng")

    user.status = payload.status
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}/password")
def update_user_password(
    user_id: uuid.UUID,
    payload: UpdatePasswordPayload,
    db: DbSession = Depends(get_db),
):
    """Admin đổi mật khẩu cho nhân viên."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng")

    if not payload.new_password or len(payload.new_password) < 6:
        raise HTTPException(status_code=400, detail="Mật khẩu mới phải có tối thiểu 6 ký tự")

    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": f"Đã cập nhật mật khẩu mới cho tài khoản {user.email}"}

