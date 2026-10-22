from datetime import date as date_type

from fastapi import APIRouter, HTTPException, Query

from app.ml_engine.predict import predict_occupancy, predict_full_day
from app.schemas.predict import PredictResponse, PredictDayResponse, HourlyPrediction

router = APIRouter(prefix="/api/predict-occupancy", tags=["machine-learning"])


@router.get("", response_model=PredictResponse)
def predict_single_hour(
    date: date_type = Query(..., description="Ngày muốn dự báo, định dạng YYYY-MM-DD"),
    hour_of_day: int = Query(..., ge=0, le=23, description="Giờ trong ngày (0-23)"),
    is_holiday: bool = Query(False, description="Có phải ngày lễ không"),
):
    """
    Dự báo tỷ lệ lấp đầy cho 1 thời điểm cụ thể. day_of_week và is_weekend được
    tự động tính từ `date` - Frontend chỉ cần gửi ngày + giờ, không cần tự tính.
    """
    day_of_week = date.weekday()  # 0=Monday ... 6=Sunday
    is_weekend = day_of_week >= 5

    try:
        rate = predict_occupancy(hour_of_day, day_of_week, is_weekend, is_holiday)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return PredictResponse(
        date=date,
        hour_of_day=hour_of_day,
        day_of_week=day_of_week,
        is_weekend=is_weekend,
        is_holiday=is_holiday,
        predicted_occupancy_rate=rate,
    )


@router.get("/day", response_model=PredictDayResponse)
def predict_whole_day(
    date: date_type = Query(..., description="Ngày muốn dự báo, định dạng YYYY-MM-DD"),
    is_holiday: bool = Query(False, description="Có phải ngày lễ không"),
):
    """Dự báo tỷ lệ lấp đầy cho cả 24 giờ trong ngày - dùng vẽ biểu đồ ở Frontend."""
    day_of_week = date.weekday()
    is_weekend = day_of_week >= 5

    try:
        forecast = predict_full_day(day_of_week, is_weekend, is_holiday)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return PredictDayResponse(
        date=date,
        day_of_week=day_of_week,
        is_weekend=is_weekend,
        is_holiday=is_holiday,
        hourly_forecast=[HourlyPrediction(**h) for h in forecast],
    )
