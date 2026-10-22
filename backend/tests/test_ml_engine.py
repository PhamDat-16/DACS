"""
Unit test cho phần logic ML thuần túy - KHÔNG cần PostgreSQL.

Chạy: pytest tests/test_ml_engine.py -v
"""

import pandas as pd

from app.ml_engine.data_generator import generate_synthetic_records
from app.ml_engine.train import train_from_dataframe, FEATURE_COLUMNS


def _make_dataframe(days=180, seed=42):
    records = generate_synthetic_records(days=days, seed=seed)
    df = pd.DataFrame(records)
    df["is_weekend"] = df["is_weekend"].astype(int)
    df["is_holiday"] = df["is_holiday"].astype(int)
    return df


def test_generate_synthetic_records_shape_and_range():
    records = generate_synthetic_records(days=10, seed=1)
    assert len(records) == 10 * 24

    for r in records:
        assert 0.0 <= r["occupancy_rate"] <= 1.0
        assert 0 <= r["hour_of_day"] <= 23
        assert 0 <= r["day_of_week"] <= 6


def test_generate_synthetic_records_is_deterministic_with_seed():
    """Cùng seed phải cho ra cùng kết quả - quan trọng để tái lập kết quả (reproducibility)."""
    records1 = generate_synthetic_records(days=5, seed=99)
    records2 = generate_synthetic_records(days=5, seed=99)
    rates1 = [r["occupancy_rate"] for r in records1]
    rates2 = [r["occupancy_rate"] for r in records2]
    assert rates1 == rates2


def test_night_hours_have_lower_average_occupancy_than_peak_hours():
    """
    Kiểm tra tính hợp lý của dữ liệu: giờ đêm (2-4h) phải có tỷ lệ lấp đầy
    trung bình THẤP HƠN RÕ RỆT so với giờ cao điểm chiều (17-18h) trên ngày thường.
    """
    df = _make_dataframe(days=180)
    weekday_df = df[df["is_weekend"] == 0]

    night_avg = weekday_df[weekday_df["hour_of_day"].isin([2, 3, 4])]["occupancy_rate"].mean()
    peak_avg = weekday_df[weekday_df["hour_of_day"].isin([17, 18])]["occupancy_rate"].mean()

    assert night_avg < peak_avg
    assert peak_avg > 0.7  # giờ cao điểm phải ở mức cao
    assert night_avg < 0.25  # giờ đêm phải ở mức thấp


def test_model_trains_and_predicts_within_valid_range():
    df = _make_dataframe(days=180)
    model, metrics = train_from_dataframe(df)

    assert metrics["mae"] < 0.15  # model phải học được pattern với sai số chấp nhận được
    assert metrics["train_size"] > 0
    assert metrics["test_size"] > 0

    sample = pd.DataFrame([[18, 1, 0, 0]], columns=FEATURE_COLUMNS)
    prediction = model.predict(sample)[0]
    assert 0.0 <= prediction <= 1.0


def test_model_learns_peak_hour_pattern():
    """Model phải dự báo giờ cao điểm (18h) CAO HƠN giờ đêm (3h) trên cùng 1 ngày thường."""
    df = _make_dataframe(days=180)
    model, _ = train_from_dataframe(df)

    night_pred = model.predict(pd.DataFrame([[3, 1, 0, 0]], columns=FEATURE_COLUMNS))[0]
    peak_pred = model.predict(pd.DataFrame([[18, 1, 0, 0]], columns=FEATURE_COLUMNS))[0]

    assert peak_pred > night_pred
