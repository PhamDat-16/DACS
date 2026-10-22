import uuid
from typing import List, Tuple

from pydantic import BaseModel


class NavigateResponse(BaseModel):
    slot_id: uuid.UUID
    slot_code: str
    path: List[Tuple[int, int]]  # danh sách tọa độ (x, y) theo thứ tự đi qua
    total_steps: int
