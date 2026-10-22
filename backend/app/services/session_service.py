from datetime import datetime, timezone
from typing import Optional
import uuid
import re

from fastapi import HTTPException
from sqlalchemy.orm import Session as DbSession

from app.models.booking import Booking, BookingStatus
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.models.parking_lot import ParkingLot
from app.models.vehicle import Vehicle, VehicleType
from app.models.session import ParkingSession, SessionStatus
from app.models.user import User
from app.routers.analytics import check_monthly_pass_by_plate, normalize_plate


def check_in(
    db: DbSession,
    staff: User,
    qr_code: Optional[str] = None,
    license_plate: Optional[str] = None,
    slot_id: Optional[uuid.UUID] = None,
    slot_code: Optional[str] = None,
    lot_name: Optional[str] = None,
) -> ParkingSession:
    """
    Quy trình check-in:
    1. Quét mã QR Booking của khách (Booking Check-in).
    2. Hoặc nhận diện biển số xe (Camera / Nhân viên nhập):
       - Nếu có Vé tháng VIP hợp lệ: Miễn phí 100% (0đ), vào tự do không cần Booking trước.
       - Nếu khách vãng lai: Tự động xếp chỗ hoặc nhận theo vị trí ô đỗ được chọn.
    """
    now_utc = datetime.now(timezone.utc)

    # 1. Trường hợp có mã QR đặt chỗ trước (Booking QR)
    if qr_code and not license_plate:
        booking = (
            db.query(Booking)
            .filter(Booking.qr_code == qr_code)
            .with_for_update()
            .first()
        )
        if not booking:
            # Thử tìm theo mã booking BKxxxxx nếu qr_code truyền dạng BKxxxxx
            booking = (
                db.query(Booking)
                .filter(Booking.id == uuid.UUID(qr_code) if len(qr_code) == 36 else False)
                .with_for_update()
                .first()
            )

        if not booking:
            raise HTTPException(status_code=404, detail="Mã QR không hợp lệ hoặc không tồn tại")

        if booking.status != BookingStatus.confirmed:
            raise HTTPException(
                status_code=400,
                detail=f"Booking đang ở trạng thái '{booking.status.value}', không thể check-in",
            )

        slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.slot_id).with_for_update().first()
        if not slot:
            raise HTTPException(status_code=404, detail="Không tìm thấy ô đỗ được gắn với booking")

        # Kiểm tra phương tiện của booking có đang trong phiên đỗ chưa check-out không
        plate_str = booking.vehicle.license_plate if booking.vehicle else None
        if plate_str or booking.vehicle_id:
            norm_bk_plate = normalize_plate(plate_str) if plate_str else ""
            active_bk_sessions = (
                db.query(ParkingSession)
                .filter(
                    ParkingSession.status.in_([SessionStatus.PARKING, SessionStatus.parking]),
                    ParkingSession.check_out_time.is_(None)
                )
                .all()
            )
            for s in active_bk_sessions:
                s_plate = s.vehicle.license_plate if s.vehicle else ""
                if (booking.vehicle_id and s.vehicle_id == booking.vehicle_id) or (norm_bk_plate and s_plate and normalize_plate(s_plate) == norm_bk_plate):
                    s_code = s.slot.slot_code if s.slot else "N/A"
                    s_lot = s.slot.lot.name if (s.slot and s.slot.lot) else "Bãi đỗ"
                    cin_str = s.check_in_time.strftime("%H:%M %d/%m/%Y") if s.check_in_time else ""
                    time_txt = f" (Check-in lúc {cin_str})" if cin_str else ""
                    raise HTTPException(
                        status_code=400,
                        detail=f"Phương tiện {plate_str or 'của booking'} hiện đang đỗ tại ô {s_code} ({s_lot}){time_txt}, chưa thực hiện check-out xuất bến!",
                    )

        # Kiểm tra ưu đãi vé tháng
        is_free = False
        note_text = "Check-in qua Booking QR"
        if plate_str:
            pass_check = check_monthly_pass_by_plate(plate_str)
            if pass_check.get("has_valid_pass"):
                is_free = True
                note_text = "👑 Thuê bao Vé tháng VIP (0 VNĐ)"

        session = ParkingSession(
            booking_id=booking.id,
            vehicle_id=booking.vehicle_id,
            slot_id=slot.id,
            check_in_time=now_utc,
            check_in_by=staff.id,
            handled_by_staff=staff.email,
            status=SessionStatus.PARKING,
            total_fee=0 if is_free else 0,
            note=note_text,
        )
        slot.status = SlotStatus.occupied
        db.add(session)
        db.add(slot)
        db.commit()
        db.refresh(session)
        return session

    # 2. Trường hợp check-in trực tiếp qua Biển số xe (Vé tháng hoặc Vãng lai)
    plate_to_use = license_plate
    if not plate_to_use and qr_code:
        # Nếu qr_code chứa format SP-QR-xxx-xxx
        parts = qr_code.split("-")
        if len(parts) >= 3:
            plate_to_use = parts[-1]

    if not plate_to_use:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp mã QR hoặc Biển số xe để check-in")

    clean_plate = plate_to_use.strip().upper()
    pass_check = check_monthly_pass_by_plate(clean_plate)
    has_valid_pass = pass_check.get("has_valid_pass", False)

    # Tìm hoặc tạo hồ sơ phương tiện trong database
    veh = db.query(Vehicle).filter(Vehicle.license_plate == clean_plate).first()
    if not veh:
        owner_name = pass_check.get("pass", {}).get("owner_name") or "Khách vào bãi"
        owner_phone = pass_check.get("pass", {}).get("phone")
        v_type_str = pass_check.get("pass", {}).get("vehicle_type") or ("motorcycle" if any(k in clean_plate.lower() for k in ["a", "b", "moto"]) else "car")
        veh_type = VehicleType.motorcycle if v_type_str == "moto" or v_type_str == "motorcycle" else VehicleType.car
        veh = Vehicle(
            license_plate=clean_plate,
            vehicle_type=veh_type,
            owner_name=owner_name,
            owner_phone=owner_phone,
        )
        db.add(veh)
        db.flush()

    # Kiểm tra phương tiện này có phiên đỗ xe đang mở không (chống check-in trùng)
    clean_norm_plate = normalize_plate(clean_plate)
    active_sessions = (
        db.query(ParkingSession)
        .filter(
            ParkingSession.status.in_([SessionStatus.PARKING, SessionStatus.parking]),
            ParkingSession.check_out_time.is_(None)
        )
        .all()
    )
    for s in active_sessions:
        s_plate = s.vehicle.license_plate if s.vehicle else ""
        if (s.vehicle_id == veh.id) or (s_plate and normalize_plate(s_plate) == clean_norm_plate):
            s_code = s.slot.slot_code if s.slot else "N/A"
            s_lot = s.slot.lot.name if (s.slot and s.slot.lot) else "Bãi đỗ"
            cin_str = s.check_in_time.strftime("%H:%M %d/%m/%Y") if s.check_in_time else ""
            time_txt = f" (Check-in lúc {cin_str})" if cin_str else ""
            raise HTTPException(
                status_code=400,
                detail=f"Phương tiện {clean_plate} hiện đang đỗ tại ô {s_code} ({s_lot}){time_txt}, chưa thực hiện check-out xuất bến!",
            )

    # Xác định Slot đỗ
    slot = None
    if slot_id:
        slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).with_for_update().first()
    elif slot_code:
        c_code = slot_code.strip().upper()
        slot_query = db.query(ParkingSlot).filter(ParkingSlot.slot_code == c_code)
        if lot_name:
            slot_query = slot_query.join(ParkingLot).filter(ParkingLot.name.ilike(f"%{lot_name.strip()}%"))
        slot = slot_query.with_for_update().first()
        if not slot:
            c_code_clean = c_code.replace("-", "")
            slot = db.query(ParkingSlot).filter(ParkingSlot.slot_code == c_code_clean).with_for_update().first()

    if not slot:
        # Tự động tìm 1 ô available gần nhất
        slot = db.query(ParkingSlot).filter(
            ParkingSlot.status == SlotStatus.available,
            ParkingSlot.is_obstacle == False
        ).with_for_update().first()

    if not slot:
        raise HTTPException(status_code=400, detail="Bãi đỗ đã kín chỗ, không còn vị trí trống khả dụng!")

    cur_lot_id = str(slot.lot_id) if slot and slot.lot_id else None
    cur_lot_name = slot.lot.name if (slot and slot.lot) else lot_name
    pass_check = check_monthly_pass_by_plate(clean_plate, lot_id=cur_lot_id, lot_name=cur_lot_name)
    has_valid_pass = pass_check.get("has_valid_pass", False)
    is_wrong_lot = pass_check.get("is_wrong_lot", False)

    if has_valid_pass:
        note_text = f"👑 Thuê bao Vé tháng VIP - Vào tự do (0 VNĐ) [{cur_lot_name or 'Đúng bãi'}]"
    elif is_wrong_lot:
        reg_lot = pass_check.get("registered_lot_name") or "Bãi khác"
        note_text = f"Xe có Vé tháng tại {reg_lot} - Đỗ tại {cur_lot_name or 'bãi này'} tính cước vãng lai"
    else:
        staff_name = staff.full_name or staff.username or staff.email
        staff_shift = staff.shift or "Ca trực"
        note_text = f"Đăng ký trực tiếp bởi nhân viên {staff_name} ({staff_shift})"

    session = ParkingSession(
        vehicle_id=veh.id,
        slot_id=slot.id,
        check_in_time=now_utc,
        check_in_by=staff.id,
        handled_by_staff=staff.email,
        status=SessionStatus.PARKING,
        total_fee=0,
        note=note_text,
    )
    slot.status = SlotStatus.occupied
    db.add(session)
    db.add(slot)
    db.commit()
    db.refresh(session)
    return session


def check_out(
    db: DbSession,
    session_id: Optional[uuid.UUID] = None,
    license_plate: Optional[str] = None,
    staff: Optional[User] = None,
) -> ParkingSession:
    """
    Kết thúc phiên đỗ xe:
    - Nếu xe có vé tháng hợp lệ TẠI ĐÚNG BÃI ĐỖ: Tổng tiền = 0 VNĐ (Miễn phí 100%).
    - Nếu xe vãng lai/vé hết hạn/vé thuộc bãi khác: Tính tiền theo giờ thực tế (30.000 VNĐ/h).
    - Giải phóng ô đỗ về 'available'.
    """
    session = None
    if session_id:
        session = db.query(ParkingSession).filter(ParkingSession.id == session_id).with_for_update().first()
    elif license_plate:
        clean_plate = license_plate.strip().upper()
        veh = db.query(Vehicle).filter(Vehicle.license_plate == clean_plate).first()
        if veh:
            session = (
                db.query(ParkingSession)
                .filter(
                    ParkingSession.vehicle_id == veh.id,
                    ParkingSession.status == SessionStatus.PARKING,
                    ParkingSession.check_out_time.is_(None)
                )
                .with_for_update()
                .first()
            )

    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên đỗ xe đang mở tương ứng")

    if session.check_out_time is not None:
        raise HTTPException(status_code=400, detail="Phiên đỗ xe này đã hoàn tất check-out trước đó")

    slot = db.query(ParkingSlot).filter(ParkingSlot.id == session.slot_id).with_for_update().first()

    now_utc = datetime.now(timezone.utc)
    session.check_out_time = now_utc
    if staff:
        session.check_out_by = staff.id

    # Xác định biển số xe để kiểm tra quyền lợi vé tháng
    plate = None
    if session.vehicle:
        plate = session.vehicle.license_plate
    elif session.booking and session.booking.vehicle:
        plate = session.booking.vehicle.license_plate

    cur_lot_id = str(slot.lot_id) if slot and slot.lot_id else None
    cur_lot_name = slot.lot.name if (slot and slot.lot) else None
    is_free = False
    is_wrong_lot = False
    reg_lot_name = None

    if plate:
        pass_check = check_monthly_pass_by_plate(plate, lot_id=cur_lot_id, lot_name=cur_lot_name)
        if pass_check.get("has_valid_pass") and pass_check.get("is_free"):
            is_free = True
        elif pass_check.get("is_wrong_lot"):
            is_wrong_lot = True
            reg_lot_name = pass_check.get("registered_lot_name")

    if is_free:
        session.total_fee = 0
        session.note = (session.note or "") + " [👑 Vé tháng VIP - Miễn phí 0 VNĐ]"
    else:
        # Tính cước theo 30.000 VNĐ/h, tối thiểu 1 giờ
        diff_hours = max(1, int((now_utc - session.check_in_time).total_seconds() / 3600))
        session.total_fee = diff_hours * 30000
        if is_wrong_lot:
            session.note = (session.note or "") + f" [Vé tháng tại {reg_lot_name} - Tính giờ tại bãi này]"

    session.status = SessionStatus.COMPLETED

    if slot:
        slot.status = SlotStatus.available

    if session.booking_id:
        booking = db.query(Booking).filter(Booking.id == session.booking_id).first()
        if booking:
            booking.status = BookingStatus.completed

    db.commit()
    db.refresh(session)
    return session

