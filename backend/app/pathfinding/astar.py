"""
Cài đặt thuật toán A* (A-star) - tìm đường đi ngắn nhất trên lưới 2D.

Ý tưởng cốt lõi của A*:
- Đây là thuật toán tìm đường có "định hướng" (informed search), khác với Dijkstra
  hay BFS vốn dò tất cả các hướng như nhau.
- Với mỗi ô đang xét, A* tính điểm:  f(n) = g(n) + h(n)
    - g(n): chi phí THỰC TẾ đã đi từ điểm bắt đầu tới ô n
    - h(n): chi phí ƯỚC LƯỢNG (heuristic) từ ô n tới đích - ở đây dùng khoảng
      cách Manhattan (|dx| + |dy|), phù hợp vì xe chỉ đi ngang/dọc theo lưới ô vuông.
- A* luôn ưu tiên mở rộng ô có f(n) nhỏ nhất trước (dùng priority queue/heap),
  nên nó "hướng" nhanh về phía đích thay vì dò lan tỏa đều như BFS/Dijkstra
  => nhanh hơn đáng kể trên bản đồ lớn mà vẫn đảm bảo tìm ra đường đi NGẮN NHẤT
  (vì heuristic Manhattan không bao giờ đánh giá cao hơn chi phí thực - gọi là
  "admissible heuristic", điều kiện bắt buộc để A* cho kết quả tối ưu).
"""

import heapq
from typing import Dict, List, Optional

from app.pathfinding.grid import Grid, Coordinate


def manhattan_distance(a: Coordinate, b: Coordinate) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(grid: Grid, start: Coordinate, goal: Coordinate) -> Optional[List[Coordinate]]:
    """
    Trả về danh sách tọa độ từ start -> goal (bao gồm cả 2 đầu), theo thứ tự đi qua.
    Trả về None nếu không tồn tại đường đi (bị chặn hoàn toàn bởi obstacle).
    """
    if not grid.is_walkable(start) or not grid.is_walkable(goal):
        return None
    if start == goal:
        return [start]

    # open_set: hàng đợi ưu tiên (min-heap) chứa (f_score, tie_breaker, node)
    # tie_breaker dùng để tránh so sánh trực tiếp 2 tuple Coordinate khi f_score bằng nhau
    counter = 0
    open_set: List[tuple] = []
    heapq.heappush(open_set, (0, counter, start))

    came_from: Dict[Coordinate, Coordinate] = {}
    g_score: Dict[Coordinate, int] = {start: 0}
    visited: set = set()

    while open_set:
        _current_f, _, current = heapq.heappop(open_set)

        if current == goal:
            return _reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for neighbor in grid.neighbors(current):
            tentative_g = g_score[current] + 1  # mỗi bước di chuyển tốn 1 đơn vị chi phí

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor, goal)
                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))

    return None  # duyệt hết open_set mà không tới được goal => không có đường đi


def _reconstruct_path(came_from: Dict[Coordinate, Coordinate], current: Coordinate) -> List[Coordinate]:
    """Truy vết ngược từ đích về điểm xuất phát qua dict came_from, rồi đảo lại thứ tự."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
