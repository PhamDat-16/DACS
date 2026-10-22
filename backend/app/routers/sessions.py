from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session as DbSession
from sqlalchemy import or_

from app.core.database import get_db
from app.core.deps import require_role, get_current_user
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.models.vehicle import Vehicle
from app.models.booking import Booking
from app.schemas.session import CheckInRequest, CheckOutRequest, SessionOut
from app.services.session_service import check_in, check_out

from typing import List, Optional
import uuid
from app.models.session import ParkingSession

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _extract_optional_user(request: Request, db: DbSession) -> Optional[User]:
    """Trích xuất User từ Bearer token nếu có (không bắt buộc ném 401 nếu không có header)."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
        decoded = decode_access_token(token)
        if decoded and "sub" in decoded:
            try:
                user_id = uuid.UUID(str(decoded["sub"]))
                return db.query(User).filter(User.id == user_id).first()
            except Exception:
                pass
    return None


@router.get("/my-history", response_model=List[SessionOut])
def get_my_sessions(
    current_user: User = Depends(get_current_user),
    db: DbSession = Depends(get_db),
):
    """
    Lấy lịch sử gửi xe của CHÍNH CÁ NHÂN KHÁCH HÀNG hiện tại.
    Khách hàng chỉ xem được các phiên đỗ của xe thuộc tài khoản mình hoặc booking của mình.
    """
    user_vehicle_ids = [v.id for v in db.query(Vehicle.id).filter(Vehicle.user_id == current_user.id).all()]
    user_booking_ids = [b.id for b in db.query(Booking.id).filter(Booking.user_id == current_user.id).all()]

    conditions = []
    if user_vehicle_ids:
        conditions.append(ParkingSession.vehicle_id.in_(user_vehicle_ids))
    if user_booking_ids:
        conditions.append(ParkingSession.booking_id.in_(user_booking_ids))

    if not conditions:
        return []

    sessions = (
        db.query(ParkingSession)
        .filter(or_(*conditions))
        .order_by(ParkingSession.check_in_time.desc())
        .limit(100)
        .all()
    )
    return sessions


def _get_current_user_optional(
    request: Request,
    db: DbSession = Depends(get_db),
) -> Optional[User]:
    return _extract_optional_user(request, db)


@router.get("", response_model=List[SessionOut])
def get_sessions(
    request: Request = None,
    current_user: Optional[User] = Depends(_get_current_user_optional),
    db: DbSession = Depends(get_db),
):
    """
    Lấy danh sách các phiên đỗ xe:
    - Admin & Staff: Xem được toàn bộ phiên đỗ xe của hệ thống (phục vụ giám sát, bốt bảo vệ).
    - Customer: Chỉ xem được các phiên đỗ xe của chính cá nhân mình (cách ly bảo mật).
    - Khách chưa đăng nhập: Trả về rỗng hoặc chỉ xem phiên nếu được truyền quyền.
    """
    user = current_user
    if not user and request:
        user = _extract_optional_user(request, db)
    query = db.query(ParkingSession)

    # Phân quyền truy cập danh sách phiên đỗ xe:
    # - Nếu là Khách hàng (Customer): Bắt buộc chỉ được xem các phiên của xe hoặc booking của cá nhân mình.
    # - Nếu là Admin, Staff hoặc màn hình Barrier / Điều phối bãi: Xem được toàn bộ phiên để phục vụ kiểm soát ra/vào và thanh toán check-out.
    if user and user.role == UserRole.customer:
        user_vehicle_ids = [v.id for v in db.query(Vehicle.id).filter(Vehicle.user_id == user.id).all()]
        user_booking_ids = [b.id for b in db.query(Booking.id).filter(Booking.user_id == user.id).all()]
        conditions = []
        if user_vehicle_ids:
            conditions.append(ParkingSession.vehicle_id.in_(user_vehicle_ids))
        if user_booking_ids:
            conditions.append(ParkingSession.booking_id.in_(user_booking_ids))
        if not conditions:
            return []
        query = query.filter(or_(*conditions))

    sessions = (
        query
        .order_by(ParkingSession.check_in_time.desc())
        .limit(100)
        .all()
    )
    return sessions


@router.post("/check-in", response_model=SessionOut)
def staff_check_in(
    payload: CheckInRequest,
    current_staff: User = Depends(require_role(UserRole.staff, UserRole.admin)),
    db: DbSession = Depends(get_db),
):
    plate = payload.license_plate or payload.plate
    return check_in(
        db,
        staff=current_staff,
        qr_code=payload.qr_code,
        license_plate=plate,
        slot_id=payload.slot_id,
        slot_code=payload.slot_code,
        lot_name=payload.lot_name,
    )


@router.post("/check-out", response_model=SessionOut)
def staff_check_out(
    payload: CheckOutRequest,
    current_staff: User = Depends(require_role(UserRole.staff, UserRole.admin)),
    db: DbSession = Depends(get_db),
):
    plate = payload.license_plate or payload.plate
    return check_out(db, session_id=payload.session_id, license_plate=plate, staff=current_staff)

