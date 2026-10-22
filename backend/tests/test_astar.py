"""
Unit test cho thuật toán A* - chạy độc lập, KHÔNG cần database/PostgreSQL.

Chạy: pytest tests/test_astar.py -v
"""

from app.pathfinding.grid import Grid
from app.pathfinding.astar import find_path, manhattan_distance


def test_straight_line_no_obstacle():
    """Đường thẳng không vật cản: đường đi phải có độ dài đúng bằng khoảng cách Manhattan + 1."""
    grid = Grid(width=5, height=5, obstacles=set())
    path = find_path(grid, (0, 0), (4, 0))
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (4, 0)
    assert len(path) == 5  # đi qua đúng 5 ô: (0,0)(1,0)(2,0)(3,0)(4,0)


def test_path_avoids_obstacles():
    """A* phải né được vật cản thay vì đi xuyên qua."""
    # Lưới 3x3, cột giữa (x=1) bị chặn hoàn toàn từ y=0 đến y=1
    grid = Grid(width=3, height=3, obstacles={(1, 0), (1, 1)})
    path = find_path(grid, (0, 0), (2, 0))

    assert path is not None
    # Đường đi không được đi qua bất kỳ ô obstacle nào
    for point in path:
        assert point not in grid.obstacles


def test_no_path_when_fully_blocked():
    """Nếu đích bị bao vây hoàn toàn bởi obstacle, phải trả về None (không có đường đi)."""
    grid = Grid(
        width=3,
        height=3,
        obstacles={(0, 1), (1, 0), (2, 1), (1, 2)},  # bao quanh hết 4 hướng của (1,1)
    )
    path = find_path(grid, (0, 0), (1, 1))
    assert path is None


def test_start_equals_goal():
    grid = Grid(width=3, height=3, obstacles=set())
    path = find_path(grid, (1, 1), (1, 1))
    assert path == [(1, 1)]


def test_path_is_optimal_shortest_length():
    """
    A* phải tìm đường NGẮN NHẤT, không phải đường bất kỳ.
    Với lưới trống, số bước đi luôn bằng đúng khoảng cách Manhattan.
    """
    grid = Grid(width=10, height=10, obstacles=set())
    start, goal = (0, 0), (6, 4)
    path = find_path(grid, start, goal)

    expected_steps = manhattan_distance(start, goal)
    assert len(path) - 1 == expected_steps  # số cạnh đi qua = số ô - 1


def test_goal_or_start_is_obstacle_returns_none():
    grid = Grid(width=3, height=3, obstacles={(2, 2)})
    assert find_path(grid, (0, 0), (2, 2)) is None
