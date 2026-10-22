import string

from sqlalchemy.orm import Session as DbSession

from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot
from app.schemas.parking_lot import ParkingLotCreate


def _slot_code(x: int, y: int) -> str:
    """Sinh mã slot kiểu 'A1', 'B12'... từ tọa độ (cột chữ cái, hàng số)."""
    if y < 26:
        col_letter = string.ascii_uppercase[y]
    else:
        # Vượt quá 26 hàng thì lặp lại chữ cái (AA, AB...) - hiếm khi xảy ra với bãi xe thường
        col_letter = string.ascii_uppercase[y // 26 - 1] + string.ascii_uppercase[y % 26]
    return f"{col_letter}{x + 1}"


def create_lot_with_grid(db: DbSession, payload: ParkingLotCreate) -> ParkingLot:
    """
    Tạo 1 ParkingLot và tự động sinh toàn bộ ParkingSlot theo lưới grid_width x grid_height.
    Các ô nằm trong obstacle_positions sẽ được đánh dấu is_obstacle=True (không thể đặt chỗ,
    và sau này A* ở Phase 3 sẽ né các ô này khi tìm đường).
    """
    obstacles = {(x, y) for x, y in payload.obstacle_positions}

    lot = ParkingLot(
        name=payload.name,
        address=payload.address,
        grid_width=payload.grid_width,
        grid_height=payload.grid_height,
        latitude=payload.latitude,
        longitude=payload.longitude,
        district=payload.district,
        city=payload.city or "Hà Nội",
        hourly_base_rate=payload.hourly_base_rate or 25000,
        has_ev_charging=payload.has_ev_charging if payload.has_ev_charging is not None else True,
        has_roof=payload.has_roof if payload.has_roof is not None else True,
        status=payload.status or "active",
    )
    db.add(lot)
    db.flush()  # để lấy lot.id trước khi tạo slot, chưa commit

    for y in range(payload.grid_height):
        for x in range(payload.grid_width):
            is_obstacle = (x, y) in obstacles
            slot = ParkingSlot(
                lot_id=lot.id,
                slot_code=_slot_code(x, y),
                pos_x=x,
                pos_y=y,
                is_obstacle=is_obstacle,
            )
            db.add(slot)

    db.commit()
    db.refresh(lot)
    return lot
