"""
Huấn luyện model Random Forest dự báo tỷ lệ lấp đầy bãi xe.

Chạy trực tiếp (cần đã có dữ liệu trong bảng occupancy_history):
    python -m app.ml_engine.train
"""

import os
from typing import Tuple

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

# Thứ tự cột feature PHẢI giống hệt lúc train và lúc predict - tách thành hằng số
# dùng chung ở cả train.py và predict.py để tránh lệch thứ tự gây dự báo sai.
FEATURE_COLUMNS = ["hour_of_day", "day_of_week", "is_weekend", "is_holiday"]
TARGET_COLUMN = "occupancy_rate"

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "occupancy_model.joblib")


def train_from_dataframe(df: pd.DataFrame) -> Tuple[RandomForestRegressor, dict]:
    """
    Hàm THUẦN TÚY: nhận vào 1 DataFrame đã có sẵn các cột feature + target,
    trả về (model đã train, dict metrics đánh giá). Không đụng tới DB hay file
    - vì vậy có thể unit test độc lập với dữ liệu giả bất kỳ.
    """
    X = df[FEATURE_COLUMNS].astype(float)
    y = df[TARGET_COLUMN].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(mean_squared_error(y_test, predictions) ** 0.5),
        "train_size": len(X_train),
        "test_size": len(X_test),
    }

    return model, metrics


def load_training_data_from_db() -> pd.DataFrame:
    """Đọc toàn bộ dữ liệu từ bảng occupancy_history - đây là phần DUY NHẤT cần DB."""
    # Import trong hàm (không import ở đầu file) để module này vẫn import được
    # và unit-test được (train_from_dataframe) ngay cả khi chưa cấu hình DB.
    from app.core.database import SessionLocal
    from app.models.occupancy_history import OccupancyHistory

    db = SessionLocal()
    try:
        rows = db.query(OccupancyHistory).all()
    finally:
        db.close()

    if not rows:
        raise ValueError(
            "Không có dữ liệu trong bảng occupancy_history. "
            "Hãy chạy `python -m app.ml_engine.data_generator` trước để sinh dữ liệu."
        )

    return pd.DataFrame(
        [
            {
                "hour_of_day": r.hour_of_day,
                "day_of_week": r.day_of_week,
                "is_weekend": int(r.is_weekend),
                "is_holiday": int(r.is_holiday),
                "occupancy_rate": r.occupancy_rate,
            }
            for r in rows
        ]
    )


def main():
    print("Đang đọc dữ liệu từ database...")
    df = load_training_data_from_db()
    print(f"Đã đọc {len(df)} bản ghi.")

    print("Đang huấn luyện Random Forest...")
    model, metrics = train_from_dataframe(df)

    print(f"MAE  (sai số tuyệt đối trung bình): {metrics['mae']:.4f}")
    print(f"RMSE (căn bậc 2 sai số bình phương trung bình): {metrics['rmse']:.4f}")
    print(f"Tập train: {metrics['train_size']} mẫu, tập test: {metrics['test_size']} mẫu")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Đã lưu model tại: {MODEL_PATH}")


if __name__ == "__main__":
    main()
