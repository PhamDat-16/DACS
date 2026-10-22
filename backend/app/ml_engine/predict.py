"""
Load model đã train (từ train.py) và cung cấp hàm dự báo tỷ lệ lấp đầy.
"""

import os
import threading
from typing import Optional

import joblib
import pandas as pd

from app.ml_engine.train import FEATURE_COLUMNS, MODEL_PATH

_model = None
_model_lock = threading.Lock()


def _load_model():
    """
    Lazy-load model 1 lần duy nhất (singleton), dùng lock để tránh race condition
    nếu nhiều request gọi predict cùng lúc trước khi model được load lần đầu.
    """
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:  # double-checked locking
                if not os.path.exists(MODEL_PATH):
                    raise FileNotFoundError(
                        f"Chưa có model tại {MODEL_PATH}. "
                        "Hãy chạy `python -m app.ml_engine.train` trước."
                    )
                _model = joblib.load(MODEL_PATH)
    return _model


def predict_occupancy(
    hour_of_day: int, day_of_week: int, is_weekend: bool, is_holiday: bool = False
) -> float:
    """
    Dự báo tỷ lệ lấp đầy (0.0 - 1.0) cho 1 thời điểm cụ thể.
    Input được đóng gói thành DataFrame với đúng tên cột như lúc train,
    tránh warning "X does not have valid feature names" của scikit-learn.
    """
    model = _load_model()

    X = pd.DataFrame(
        [[hour_of_day, day_of_week, int(is_weekend), int(is_holiday)]],
        columns=FEATURE_COLUMNS,
    )
    prediction = model.predict(X)[0]
    return float(max(0.0, min(1.0, prediction)))  # clip về [0,1] cho an toàn


def predict_full_day(day_of_week: int, is_weekend: bool, is_holiday: bool = False):
    """Dự báo cho cả 24 giờ trong ngày - dùng để vẽ biểu đồ dự báo cả ngày ở Frontend."""
    return [
        {
            "hour_of_day": h,
            "predicted_occupancy_rate": predict_occupancy(h, day_of_week, is_weekend, is_holiday),
        }
        for h in range(24)
    ]
