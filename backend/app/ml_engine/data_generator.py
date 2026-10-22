"""
Sinh dữ liệu lịch sử tỷ lệ lấp đầy bãi xe - GIẢ LẬP (synthetic) nhưng có quy luật
thực tế, để model ML học được pattern có ý nghĩa thay vì nhiễu ngẫu nhiên vô nghĩa.

Quy luật được mô phỏng:
- Ban đêm (0h-5h): lấp đầy rất thấp (~5-15%) - hầu như không ai gửi xe qua đêm.
- Giờ cao điểm sáng (7h-9h): tăng vọt (~65-90%) - giờ đi làm/đi học.
- Giữa ngày (10h-16h): mức trung bình (~40-60%).
- Giờ cao điểm chiều (17h-19h): cao nhất trong ngày (~75-95%) - giờ tan tầm.
- Tối muộn (20h-23h): giảm dần về đêm.
- Cuối tuần (T7, CN): toàn bộ pattern bị "làm phẳng" hơn - không có cao điểm rõ
  rệt như ngày thường vì không có giờ đi làm/đi học cố định, và mức nền thấp hơn.
- Ngày lễ (is_holiday): tương tự cuối tuần nhưng mức nền cao hơn 1 chút (đi chơi lễ).
- Nhiễu Gaussian được cộng thêm vào mỗi điểm dữ liệu để mô phỏng biến động thực tế
  (thời tiết, sự kiện bất thường...), rồi giới hạn (clip) về khoảng [0, 1].
"""

import random
from datetime import datetime, timedelta, timezone
from typing import List, Dict


def _base_occupancy_weekday(hour: int) -> float:
    """Đường cong lấp đầy chuẩn cho NGÀY THƯỜNG theo giờ trong ngày."""
    if 0 <= hour < 6:
        return 0.10
    if 6 <= hour < 7:
        return 0.30
    if 7 <= hour < 9:
        return 0.80
    if 9 <= hour < 11:
        return 0.60
    if 11 <= hour < 14:
        return 0.55
    if 14 <= hour < 17:
        return 0.50
    if 17 <= hour < 19:
        return 0.88
    if 19 <= hour < 21:
        return 0.55
    return 0.25  # 21h-23h


def _base_occupancy_weekend(hour: int) -> float:
    """Đường cong lấp đầy chuẩn cho CUỐI TUẦN - phẳng hơn, mức nền thấp hơn."""
    if 0 <= hour < 8:
        return 0.08
    if 8 <= hour < 11:
        return 0.35
    if 11 <= hour < 20:
        return 0.50  # mức trung bình kéo dài cả ngày, không có đỉnh nhọn
    return 0.20


def generate_synthetic_records(
    days: int = 90,
    noise_std: float = 0.06,
    holiday_probability: float = 0.03,
    seed: int = 42,
) -> List[Dict]:
    """
    Sinh ra danh sách dict dữ liệu lịch sử cho `days` ngày gần nhất, mỗi ngày 24 bản ghi
    (1 bản ghi/giờ). Hàm THUẦN TÚY - không đụng tới database - để dễ unit test.

    Trả về list các dict với đúng các trường cần thiết để tạo OccupancyHistory:
    hour_of_day, day_of_week, is_weekend, is_holiday, occupancy_rate, recorded_at
    """
    rng = random.Random(seed)
    records: List[Dict] = []

    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)

    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        day_of_week = current_date.weekday()  # 0=Monday ... 6=Sunday
        is_weekend = day_of_week >= 5
        is_holiday = rng.random() < holiday_probability

        for hour in range(24):
            if is_weekend or is_holiday:
                base = _base_occupancy_weekend(hour)
                if is_holiday and not is_weekend:
                    base += 0.05  # ngày lễ giữa tuần thường đông hơn cuối tuần thường một chút
            else:
                base = _base_occupancy_weekday(hour)

            noise = rng.gauss(0, noise_std)
            occupancy_rate = max(0.0, min(1.0, base + noise))

            records.append(
                {
                    "hour_of_day": hour,
                    "day_of_week": day_of_week,
                    "is_weekend": is_weekend,
                    "is_holiday": is_holiday,
                    "occupancy_rate": round(occupancy_rate, 4),
                    "recorded_at": current_date.replace(
                        hour=hour, minute=0, second=0, microsecond=0
                    ),
                }
            )

    return records


def seed_database(lot_id: str, days: int = 90) -> int:
    """
    Sinh dữ liệu synthetic rồi ghi thẳng vào bảng occupancy_history của 1 lot cụ thể.
    Đây là phần DUY NHẤT trong file này cần kết nối DB - tách riêng khỏi
    generate_synthetic_records() (hàm thuần túy ở trên) để dễ unit test.
    """
    # Import trong hàm để phần logic sinh dữ liệu (ở trên) vẫn test được độc lập
    # mà không cần cấu hình DB.
    from app.core.database import SessionLocal
    from app.models.occupancy_history import OccupancyHistory

    records = generate_synthetic_records(days=days)
    db = SessionLocal()
    try:
        for r in records:
            db.add(OccupancyHistory(lot_id=lot_id, **r))
        db.commit()
    finally:
        db.close()

    return len(records)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Sinh dữ liệu lịch sử lấp đầy giả lập và ghi vào database"
    )
    parser.add_argument("--lot-id", required=True, help="UUID của bãi xe (lấy từ GET /api/lots)")
    parser.add_argument("--days", type=int, default=90, help="Số ngày dữ liệu lịch sử muốn sinh")
    args = parser.parse_args()

    count = seed_database(lot_id=args.lot_id, days=args.days)
    print(f"Đã sinh và lưu {count} bản ghi ({args.days} ngày x 24h) cho lot_id={args.lot_id}")
