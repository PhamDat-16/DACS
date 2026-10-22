import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session as DbSession

from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot
from app.pathfinding.grid import Grid
from app.pathfinding.astar import find_path


def build_grid_from_lot(db: DbSession, lot_id: uuid.UUID) -> Grid:
    """Chuyển dữ liệu ParkingLot + ParkingSlot trong DB thành Grid thuần Python cho A*."""
    lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    if not lot:
        raise HTTPException(status_code=404, detail="Không tìm thấy bãi xe")

    obstacle_slots = (
        db.query(ParkingSlot)
        .filter(ParkingSlot.lot_id == lot_id, ParkingSlot.is_obstacle.is_(True))
        .all()
    )
    obstacles = {(s.pos_x, s.pos_y) for s in obstacle_slots}

    return Grid(width=lot.grid_width, height=lot.grid_height, obstacles=obstacles)


def navigate_to_slot(
    db: DbSession,
    lot_id: uuid.UUID,
    slot_id: uuid.UUID,
    from_x: int = 0,
    from_y: int = 0,
):
    """
    Tìm đường đi ngắn nhất từ vị trí (from_x, from_y) - mặc định là cổng vào bãi
    tại góc (0,0) - tới slot đích bằng A*.
    """
    target_slot = db.query(ParkingSlot).filter(
        ParkingSlot.id == slot_id, ParkingSlot.lot_id == lot_id
    ).first()
    if not target_slot:
        raise HTTPException(status_code=404, detail="Không tìm thấy slot trong bãi xe này")
    if target_slot.is_obstacle:
        raise HTTPException(status_code=400, detail="Vị trí đích không hợp lệ (là vật cản)")

    grid = build_grid_from_lot(db, lot_id)
    start = (from_x, from_y)
    goal = (target_slot.pos_x, target_slot.pos_y)

    path = find_path(grid, start, goal)
    if path is None:
        raise HTTPException(
            status_code=409,
            detail="Không tìm được đường đi tới vị trí này (có thể bị vật cản chặn hoàn toàn)",
        )

    return target_slot, path
