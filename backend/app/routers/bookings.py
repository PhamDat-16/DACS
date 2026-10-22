from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session as DbSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate, BookingOut, BookingWithQR
from app.services.booking_service import create_booking, cancel_booking
from app.routers.analytics import check_monthly_pass_by_plate

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


def _to_booking_out(b: Booking, default_plate: Optional[str] = None, default_slot: Optional[str] = None) -> BookingOut:
    slot_code = (b.slot.slot_code if b.slot else default_slot) or "A-001"
    lot_name = (b.slot.lot.name if (b.slot and b.slot.lot) else "Smart Parking")
    plate = (b.vehicle.license_plate if b.vehicle else default_plate) or "Chưa rõ"
    code = f"BK{str(b.id)[:8].upper()}"
    duration_hours = 2
    if b.start_time and b.end_time:
        duration_hours = max(1, int((b.end_time - b.start_time).total_seconds() / 3600))
    fee = duration_hours * 15000

    if plate and plate != "Chưa rõ":
        cur_lot_id = str(b.slot.lot_id) if b.slot and b.slot.lot_id else None
        pass_check = check_monthly_pass_by_plate(plate, lot_id=cur_lot_id, lot_name=lot_name)
        if pass_check.get("has_valid_pass") and pass_check.get("is_free"):
            fee = 0


    return BookingOut(
        id=b.id,
        booking_id=code,
        code=code,
        slot_id=b.slot_id,
        slot_code=slot_code,
        lot_name=lot_name,
        vehicle_plate=plate,
        plate=plate,
        status=b.status,
        start_time=b.start_time,
        end_time=b.end_time,
        created_at=b.created_at,
        qr_code=b.qr_code,
        fee=fee
    )


@router.post("", response_model=BookingWithQR, status_code=201)
def create_new_booking(
    payload: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: DbSession = Depends(get_db),
):
    """
    Đặt chỗ trước cho 1 slot. Kiểm tra chống xung đột trùng khung giờ.
    Trả về kèm ảnh QR (base64) để khách lưu lại, dùng quét khi check-in tại bãi.
    """
    booking, qr_image = create_booking(db, current_user, payload)
    booking_out = _to_booking_out(
        booking,
        default_plate=payload.vehicle_plate or payload.plate,
        default_slot=payload.slot_code
    )
    return BookingWithQR(booking=booking_out, qr_code_image=qr_image)


@router.get("/me", response_model=List[BookingOut])
def list_my_bookings(
    current_user: User = Depends(get_current_user), db: DbSession = Depends(get_db)
):
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return [_to_booking_out(b) for b in bookings]


@router.get("", response_model=List[BookingOut])
def list_all_bookings(
    lot_name: Optional[str] = Query(None, description="Lọc theo tên bãi đỗ"),
    status: Optional[str] = Query(None, description="Lọc theo trạng thái"),
    current_user: User = Depends(get_current_user),
    db: DbSession = Depends(get_db)
):
    """
    Cho phép Staff và Admin xem danh sách phương tiện đặt chỗ tại bãi đỗ được chỉ định.
    """
    query = db.query(Booking)
    if status:
        query = query.filter(Booking.status == status)
    bookings = query.order_by(Booking.created_at.desc()).limit(100).all()
    results = [_to_booking_out(b) for b in bookings]
    # Phân quyền: Nhân viên bảo vệ chỉ được xem đặt chỗ tại bãi làm việc của mình
    filter_lot = lot_name
    if current_user.role == UserRole.staff and current_user.assigned_lot:
        staff_lot = current_user.assigned_lot.strip()
        if "toàn hệ thống" not in staff_lot.lower():
            filter_lot = staff_lot

    if filter_lot:
        clean_lot = filter_lot.strip().lower()
        results = [b for b in results if clean_lot in (b.lot_name or "").lower() or (b.lot_name or "").lower() in clean_lot]
    return results


@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel_my_booking(
    booking_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: DbSession = Depends(get_db),
):
    booking = cancel_booking(db, current_user, booking_id)
    return _to_booking_out(booking)

