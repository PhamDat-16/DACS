import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session as DbSession

from app.models.booking import Booking, BookingStatus
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.models.parking_lot import ParkingLot
from app.models.vehicle import Vehicle, VehicleType
from app.models.session import ParkingSession, SessionStatus
from app.models.user import User
from app.schemas.booking import BookingCreate
from app.services.qr_service import generate_booking_token, generate_qr_base64


def create_booking(db: DbSession, user: User, payload: BookingCreate) -> tuple[Booking, str]:
    """
    Tạo booking mới cho 1 slot với cơ chế chống DOUBLE-BOOKING và XUNG ĐỘT TRÙNG KHUNG GIỜ (Time-overlap conflict).

    Quy tắc nghiệp vụ:
    - Một ô đỗ chỉ được phép nhận 1 phương tiện trong 1 khung giờ.
    - Không cho phép 2 xe đặt cùng 1 ô trong khoảng thời gian trùng nhau (VD: Xe A 8h-10h, Xe B 8h-9h hoặc 9h-11h).
    - Khóa dòng ParkingSlot với row-level lock (with_for_update) để đảm bảo an toàn đồng thời.
    """
    try:
        # 1. Xác định Bãi đỗ xe mục tiêu (Target ParkingLot)
        target_lot = None
        if payload.lot_name and payload.lot_name.strip():
            clean_lot_name = payload.lot_name.strip()
            target_lot = db.query(ParkingLot).filter(ParkingLot.name.ilike(f"%{clean_lot_name}%")).first()
            if not target_lot:
                target_lot = ParkingLot(
                    name=clean_lot_name,
                    address=f"Khu vực {clean_lot_name}, Hà Nội",
                    district="Hà Đông" if "Hà Đông" in clean_lot_name else "Hà Nội",
                    city="Hà Nội",
                    grid_width=10,
                    grid_height=8,
                    hourly_base_rate=15000,
                    has_ev_charging=True,
                    has_roof=True,
                    status="active"
                )
                db.add(target_lot)
                db.flush()

        # 2. Xác định Slot trong đúng bãi đỗ xe mục tiêu
        slot = None
        if payload.slot_id:
            slot = (
                db.query(ParkingSlot)
                .filter(ParkingSlot.id == payload.slot_id)
                .with_for_update()
                .first()
            )
        elif payload.slot_code:
            clean_code = payload.slot_code.strip().upper()
            slot_query = db.query(ParkingSlot).filter(ParkingSlot.slot_code == clean_code)
            if target_lot:
                slot_query = slot_query.filter(ParkingSlot.lot_id == target_lot.id)
            slot = slot_query.with_for_update().first()
            if not slot:
                alt_code = clean_code.replace("-", "")
                alt_query = db.query(ParkingSlot).filter(ParkingSlot.slot_code == alt_code)
                if target_lot:
                    alt_query = alt_query.filter(ParkingSlot.lot_id == target_lot.id)
                slot = alt_query.with_for_update().first()

        if not slot:
            if not target_lot:
                target_lot = db.query(ParkingLot).first()

            if target_lot:
                slot_code = payload.slot_code or "A-001"
                slot = ParkingSlot(
                    lot_id=target_lot.id,
                    slot_code=slot_code,
                    vehicle_type="car",
                    pos_x=0,
                    pos_y=0,
                    status=SlotStatus.available
                )
                db.add(slot)
                db.flush()
            else:
                raise HTTPException(status_code=404, detail="Không tìm thấy vị trí đỗ xe hợp lệ")

        if slot.is_obstacle:
            raise HTTPException(status_code=400, detail="Đây không phải là vị trí đỗ xe hợp lệ")

        # 2. Chuẩn hóa thời gian bắt đầu và kết thúc
        start_time = payload.start_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)

        dur_hours = payload.duration_hours or 2
        end_time = payload.end_time
        if not end_time:
            end_time = start_time + timedelta(hours=dur_hours)
        elif end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        if end_time <= start_time:
            raise HTTPException(status_code=400, detail="Thời gian kết thúc phải sau thời gian bắt đầu")

        # Kiểm tra không cho phép đặt xe trong quá khứ (cho phép dung sai 5 phút do độ trễ truyền dữ liệu / chênh lệch đồng hồ)
        now_utc = datetime.now(timezone.utc)
        if start_time < (now_utc - timedelta(minutes=5)):
            raise HTTPException(
                status_code=400,
                detail="Thời gian bắt đầu đặt đỗ xe không thể ở trong quá khứ. Vui lòng chọn thời gian từ thời điểm hiện tại trở đi."
            )

        # 3. KIỂM TRA XUNG ĐỘT TRÙNG KHUNG GIỜ TRÊN CÙNG Ô ĐỖ (Overlapping time range conflict)
        # Điều kiện trùng: existing.start_time < new_end_time AND existing.end_time > new_start_time
        conflict_booking = (
            db.query(Booking)
            .filter(
                Booking.slot_id == slot.id,
                Booking.status.in_([BookingStatus.confirmed, BookingStatus.pending]),
                Booking.start_time < end_time,
                Booking.end_time > start_time,
            )
            .first()
        )

        if conflict_booking:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vị trí ô đỗ {slot.slot_code} này đã có người đặt trước rồi! Hệ thống đã khóa ô này để bảo mật thông tin và tránh xung đột.",
            )

        # 4. Kiểm tra xe đang đỗ trực tiếp tại ô này (active session) nếu thời gian đặt bao gồm hiện tại
        active_session = (
            db.query(ParkingSession)
            .filter(
                ParkingSession.slot_id == slot.id,
                ParkingSession.status == SessionStatus.PARKING
            )
            .first()
        )
        now = datetime.now(timezone.utc)
        if active_session and start_time <= now and end_time >= now:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ô đỗ {slot.slot_code} hiện đang có phương tiện đỗ thực tế tại bãi. Vui lòng chọn vị trí khác!",
            )

        # 5. Xử lý phương tiện (Vehicle)
        raw_plate = payload.vehicle_plate or payload.plate
        vehicle_id = payload.vehicle_id

        if raw_plate and raw_plate.strip():
            clean_plate = raw_plate.strip().upper()
            veh = db.query(Vehicle).filter(Vehicle.license_plate == clean_plate).first()
            if not veh:
                veh = Vehicle(
                    license_plate=clean_plate,
                    vehicle_type=VehicleType.motorcycle if any(k in clean_plate.lower() for k in ["a", "b", "moto"]) else VehicleType.car,
                    user_id=user.id,
                    owner_name=user.full_name or "Khách hàng",
                )
                db.add(veh)
                db.flush()
            vehicle_id = veh.id

            # Kiểm tra phương tiện này đã có lịch đặt chỗ khác trùng khung giờ chưa
            veh_conflict = (
                db.query(Booking)
                .filter(
                    Booking.vehicle_id == vehicle_id,
                    Booking.status.in_([BookingStatus.confirmed, BookingStatus.pending]),
                    Booking.start_time < end_time,
                    Booking.end_time > start_time,
                )
                .first()
            )
            if veh_conflict:
                v_start = veh_conflict.start_time.strftime("%H:%M %d/%m/%Y")
                v_end = veh_conflict.end_time.strftime("%H:%M %d/%m/%Y") if veh_conflict.end_time else ""
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Phương tiện {clean_plate} đã có lịch đặt chỗ khác trong khung giờ ({v_start} - {v_end})!",
                )

        booking_token = generate_booking_token()

        booking = Booking(
            user_id=user.id,
            slot_id=slot.id,
            vehicle_id=vehicle_id,
            qr_code=booking_token,
            status=BookingStatus.confirmed,
            start_time=start_time,
            end_time=end_time,
        )

        if start_time <= now <= end_time:
            slot.status = SlotStatus.reserved

        db.add(booking)
        db.add(slot)
        db.commit()
        db.refresh(booking)

        qr_image = generate_qr_base64(booking_token)
        return booking, qr_image

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def cancel_booking(db: DbSession, user: User, booking_id: uuid.UUID) -> Booking:
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.user_id == user.id)
        .with_for_update()
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="Không tìm thấy booking")
    if booking.status not in (BookingStatus.pending, BookingStatus.confirmed):
        raise HTTPException(status_code=400, detail="Booking này không thể hủy")

    slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.slot_id).with_for_update().first()

    booking.status = BookingStatus.cancelled
    if slot and slot.status == SlotStatus.reserved:
        slot.status = SlotStatus.available

    db.commit()
    db.refresh(booking)
    return booking
