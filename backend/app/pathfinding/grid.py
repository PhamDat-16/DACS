from dataclasses import dataclass
from typing import Set, Tuple

Coordinate = Tuple[int, int]  # (x, y)


@dataclass
class Grid:
    """
    Biểu diễn bãi xe dưới dạng lưới 2D thuần túy - không phụ thuộc SQLAlchemy/FastAPI,
    để module A* có thể test độc lập mà không cần kết nối database.
    """

    width: int
    height: int
    obstacles: Set[Coordinate]  # tập hợp các ô không thể đi qua (cột, tường...)

    def in_bounds(self, pos: Coordinate) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, pos: Coordinate) -> bool:
        return self.in_bounds(pos) and pos not in self.obstacles

    def neighbors(self, pos: Coordinate):
        """
        Trả về các ô lân cận có thể đi tới - chỉ 4 hướng (lên/xuống/trái/phải),
        KHÔNG đi chéo, vì xe di chuyển theo làn đường vuông góc, không cắt góc.
        """
        x, y = pos
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [c for c in candidates if self.is_walkable(c)]
