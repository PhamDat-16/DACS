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
    results = []
    for v in vehicles:
        vo = VehicleOut.model_validate(v)
        latest_sess = None
        if v.sessions:
            valid_sessions = [s for s in v.sessions if s.check_in_time]
            if valid_sessions:
                latest_sess = max(valid_sessions, key=lambda s: s.check_in_time)
        if latest_sess and latest_sess.check_in_time:
            vo.check_in = latest_sess.check_in_time.strftime("%H:%M")
            vo.check_in_date = latest_sess.check_in_time.strftime("%Y-%m-%d")
            if latest_sess.lot_name:
                vo.assigned_lot = latest_sess.lot_name
        results.append(vo)
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