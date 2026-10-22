import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session as DbSession

from app.core.database import get_db
from app.schemas.navigate import NavigateResponse
from app.services.navigate_service import navigate_to_slot

router = APIRouter(prefix="/api/lots/{lot_id}/navigate", tags=["navigation"])


@router.get("", response_model=NavigateResponse)
def get_navigation_path(
    lot_id: uuid.UUID,
    slot_id: uuid.UUID = Query(..., description="ID của slot muốn đến"),
    from_x: int = Query(0, description="Tọa độ x xuất phát, mặc định là cổng vào (0,0)"),
    from_y: int = Query(0, description="Tọa độ y xuất phát, mặc định là cổng vào (0,0)"),
    db: DbSession = Depends(get_db),
):
    """
    Trả về đường đi ngắn nhất (thuật toán A*) từ vị trí xuất phát tới slot đích,
    dưới dạng danh sách tọa độ - frontend dùng để vẽ đường đi trên sơ đồ bãi xe.
    """
    slot, path = navigate_to_slot(db, lot_id, slot_id, from_x, from_y)
    return NavigateResponse(
        slot_id=slot.id,
        slot_code=slot.slot_code,
        path=path,
        total_steps=len(path) - 1,
    )
