from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session as DbSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleOut, VehicleUpdate

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.get("", response_model=List[VehicleOut])
def get_vehicles(
    request: Request,
    license_plate: Optional[str] = Query(None, description="Tìm theo biển số"),
    owner_name: Optional[str] = Query(None, description="Tìm theo tên chủ xe"),
    user_id: Optional[uuid.UUID] = Query(None, description="Tìm theo ID người dùng"),
    limit: int = Query(50, ge=1, le=200),
    db: DbSession = Depends(get_db),
):
    query = db.query(Vehicle)

    target_user_id = user_id if isinstance(user_id, uuid.UUID) else (uuid.UUID(str(user_id)) if isinstance(user_id, str) and user_id.strip() else None)
    clean_plate = license_plate.strip() if isinstance(license_plate, str) and license_plate.strip() else None
    clean_owner = owner_name.strip() if isinstance(owner_name, str) and owner_name.strip() else None
    max_limit = limit if isinstance(limit, int) and limit > 0 else 50

    # Nếu client truyền header Authorization Bearer token thì tự động trích xuất user_id nếu chưa có query
    if not target_user_id and not clean_plate and not clean_owner:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            decoded = decode_access_token(token)
            if decoded and "sub" in decoded:
                try:
                    target_user_id = uuid.UUID(str(decoded["sub"]))
                except Exception:
                    pass

    if clean_plate:
        query = query.filter(Vehicle.license_plate.ilike(f"%{clean_plate}%"))
    if clean_owner:
        query = query.filter(Vehicle.owner_name.ilike(f"%{clean_owner}%"))
    vehicles = query.order_by(Vehicle.created_at.desc()).limit(max_limit).all()

    # Tải danh sách tất cả sessions để đồng bộ chính xác lịch sử đỗ xe
    from app.models.session import ParkingSession
    from app.models.booking import Booking

    all_db_sessions = db.query(ParkingSession).all()

    results = []
    for v in vehicles:
        vo = VehicleOut.model_validate(v)
        v_norm = v.license_plate.replace("-", "").replace(".", "").replace(" ", "").upper()

        # Thu thập toàn bộ phiên gửi xe thuộc về xe này
        matched_sessions = []
        seen_session_ids = set()

        # 1. Từ quan hệ trực tiếp v.sessions
        if v.sessions:
            for s in v.sessions:
                if s.id not in seen_session_ids:
                    seen_session_ids.add(s.id)
                    matched_sessions.append(s)

        # 2. Quét thêm các session khớp biển số (chuẩn hóa) nếu chưa được gắn trực tiếp vehicle_id
        for s in all_db_sessions:
            if s.id in seen_session_ids:
                continue
            s_plate = s.license_plate
            if s_plate:
                s_norm = s_plate.replace("-", "").replace(".", "").replace(" ", "").upper()
                if s_norm == v_norm:
                    seen_session_ids.add(s.id)
                    matched_sessions.append(s)
                    # Tự động liên kết vehicle_id trong DB nếu chưa có
                    if not s.vehicle_id:
                        s.vehicle_id = v.id
                        db.add(s)

        # Sắp xếp lịch sử đỗ xe theo thời gian giảm dần (mới nhất lên đầu)
        matched_sessions.sort(
            key=lambda s: s.check_in_time or s.created_at,
            reverse=True
        )

        hist_list = []
        for s in matched_sessions:
            in_str = s.check_in_time.strftime("%H:%M %d/%m/%Y") if s.check_in_time else ""
            out_str = s.check_out_time.strftime("%H:%M %d/%m/%Y") if s.check_out_time else "Đang đỗ"
            s_lot = s.lot_name or (s.slot.lot.name if s.slot and s.slot.lot else "Bãi đỗ")
            s_slot = s.slot_code or (s.slot.slot_code if s.slot else "")
            duration_str = "Đang đỗ"
            if s.check_in_time and s.check_out_time:
                diff_sec = int((s.check_out_time - s.check_in_time).total_seconds())
                h = diff_sec // 3600
                m = (diff_sec % 3600) // 60
                duration_str = f"{h}h {m:02d}m"

            hist_list.append({
                "id": str(s.id),
                "lot_name": s_lot,
                "slot_code": s_slot,
                "check_in_time": in_str,
                "check_out_time": out_str,
                "check_in_raw": s.check_in_time.isoformat() if s.check_in_time else None,
                "check_out_raw": s.check_out_time.isoformat() if s.check_out_time else None,
                "duration": duration_str,
                "status": s.status.value if hasattr(s.status, "value") else str(s.status),
                "total_fee": s.total_fee or 0,
                "handled_by_staff": s.handled_by_staff or "Nhân viên trực cổng",
                "note": s.note or ""
            })

        vo.total_sessions = len(hist_list)
        vo.sessions_history = hist_list

        if matched_sessions:
            latest_sess = matched_sessions[0]
            if latest_sess.check_in_time:
                vo.check_in = latest_sess.check_in_time.strftime("%H:%M")
                vo.check_in_date = latest_sess.check_in_time.strftime("%Y-%m-%d")
            s_lot = latest_sess.lot_name or (latest_sess.slot.lot.name if latest_sess.slot and latest_sess.slot.lot else None)
            if s_lot:
                vo.assigned_lot = s_lot
            vo.latest_slot = latest_sess.slot_code or (latest_sess.slot.slot_code if latest_sess.slot else None)
            vo.latest_status = latest_sess.status.value if hasattr(latest_sess.status, "value") else str(latest_sess.status)

        results.append(vo)

    try:
        db.commit()
    except Exception:
        db.rollback()

    return results


@router.post("", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    request: Request,
    db: DbSession = Depends(get_db),
):
    clean_plate = payload.license_plate.strip().upper()
    target_user_id = payload.user_id

    # Trích xuất user_id từ JWT Token nếu client không truyền trực tiếp trong payload
    if not target_user_id:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            decoded = decode_access_token(token)
            if decoded and "sub" in decoded:
                try:
                    target_user_id = uuid.UUID(str(decoded["sub"]))
                except Exception:
                    pass

    existing = db.query(Vehicle).filter(Vehicle.license_plate == clean_plate).first()
    if existing:
        # Nếu xe đã tồn tại trong CSDL (ví dụ từ lượt gửi cũ hoặc vãng lai):
        # Cập nhật và liên kết user_id của khách hàng hiện tại
        if target_user_id:
            existing.user_id = target_user_id
        if payload.owner_name:
            existing.owner_name = payload.owner_name
        if payload.owner_phone:
            existing.owner_phone = payload.owner_phone
        if payload.brand:
            existing.brand = payload.brand
        if payload.color:
            existing.color = payload.color
        if payload.vehicle_type:
            existing.vehicle_type = payload.vehicle_type
        db.commit()
        db.refresh(existing)
        return existing

    vehicle = Vehicle(
        license_plate=clean_plate,
        vehicle_type=payload.vehicle_type,
        brand=payload.brand,
        color=payload.color,
        owner_name=payload.owner_name,
        owner_phone=payload.owner_phone,
        user_id=target_user_id,
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.get("/{license_plate}", response_model=VehicleOut)
def get_vehicle_by_plate(
    license_plate: str,
    db: DbSession = Depends(get_db),
):
    clean_plate = license_plate.strip().upper()
    vehicle = db.query(Vehicle).filter(Vehicle.license_plate == clean_plate).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy xe {clean_plate}")
    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(
    vehicle_id: uuid.UUID,
    payload: VehicleUpdate,
    db: DbSession = Depends(get_db),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Không tìm thấy phương tiện")

    if payload.brand is not None:
        vehicle.brand = payload.brand
    if payload.color is not None:
        vehicle.color = payload.color
    if payload.owner_name is not None:
        vehicle.owner_name = payload.owner_name
    if payload.owner_phone is not None:
        vehicle.owner_phone = payload.owner_phone
    if payload.vehicle_type is not None:
        vehicle.vehicle_type = payload.vehicle_type

    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.get("/{license_plate}/sessions")
def get_vehicle_sessions(
    license_plate: str,
    db: DbSession = Depends(get_db),
):
    """
    Lấy toàn bộ lịch sử gửi đỗ xe của phương tiện theo biển số.
    """
    from app.models.session import ParkingSession

    clean_plate = license_plate.strip().upper()
    v_norm = clean_plate.replace("-", "").replace(".", "").replace(" ", "")

    vehicle = db.query(Vehicle).filter(Vehicle.license_plate == clean_plate).first()
    if not vehicle:
        # Tìm theo biển số chuẩn hóa nếu có dấu gạch ngang/chấm khác nhau
        for v in db.query(Vehicle).all():
            if v.license_plate.replace("-", "").replace(".", "").replace(" ", "").upper() == v_norm:
                vehicle = v
                break

    matched_sessions = []
    seen_ids = set()

    if vehicle and vehicle.sessions:
        for s in vehicle.sessions:
            seen_ids.add(s.id)
            matched_sessions.append(s)

    all_sessions = db.query(ParkingSession).all()
    for s in all_sessions:
        if s.id in seen_ids:
            continue
        s_plate = s.license_plate
        if s_plate and s_plate.replace("-", "").replace(".", "").replace(" ", "").upper() == v_norm:
            seen_ids.add(s.id)
            matched_sessions.append(s)

    matched_sessions.sort(
        key=lambda s: s.check_in_time or s.created_at,
        reverse=True
    )

    results = []
    for s in matched_sessions:
        in_str = s.check_in_time.strftime("%H:%M %d/%m/%Y") if s.check_in_time else ""
        out_str = s.check_out_time.strftime("%H:%M %d/%m/%Y") if s.check_out_time else "Đang đỗ"
        s_lot = s.lot_name or (s.slot.lot.name if s.slot and s.slot.lot else "Bãi đỗ")
        s_slot = s.slot_code or (s.slot.slot_code if s.slot else "")
        duration_str = "Đang đỗ"
        if s.check_in_time and s.check_out_time:
            diff_sec = int((s.check_out_time - s.check_in_time).total_seconds())
            h = diff_sec // 3600
            m = (diff_sec % 3600) // 60
            duration_str = f"{h}h {m:02d}m"

        results.append({
            "id": str(s.id),
            "lot_name": s_lot,
            "slot_code": s_slot,
            "check_in_time": in_str,
            "check_out_time": out_str,
            "check_in_raw": s.check_in_time.isoformat() if s.check_in_time else None,
            "check_out_raw": s.check_out_time.isoformat() if s.check_out_time else None,
            "duration": duration_str,
            "status": s.status.value if hasattr(s.status, "value") else str(s.status),
            "total_fee": s.total_fee or 0,
            "handled_by_staff": s.handled_by_staff or "Nhân viên trực cổng",
            "note": s.note or ""
        })

    return {
        "license_plate": clean_plate,
        "owner_name": vehicle.owner_name if vehicle else "Khách vãng lai",
        "vehicle_type": vehicle.vehicle_type.value if vehicle and hasattr(vehicle.vehicle_type, "value") else (vehicle.vehicle_type if vehicle else "car"),
        "total_sessions": len(results),
        "sessions": results
    }


@router.delete("/{vehicle_id_or_plate}")
def delete_vehicle(
    vehicle_id_or_plate: str,
    db: DbSession = Depends(get_db),
):
    vehicle = None
    try:
        val_uuid = uuid.UUID(vehicle_id_or_plate)
        vehicle = db.query(Vehicle).filter(Vehicle.id == val_uuid).first()
    except (ValueError, AttributeError):
        pass
    if not vehicle:
        clean_plate = vehicle_id_or_plate.strip().upper()
        vehicle = db.query(Vehicle).filter(Vehicle.license_plate == clean_plate).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Phương tiện không tồn tại")
    db.delete(vehicle)
    db.commit()
    return {"status": "ok", "message": "Xóa phương tiện thành công"}