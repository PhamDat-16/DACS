from datetime import date as date_type
from typing import List

from pydantic import BaseModel


class HourlyPrediction(BaseModel):
    hour_of_day: int
    predicted_occupancy_rate: float  # 0.0 - 1.0


class PredictResponse(BaseModel):
    date: date_type
    hour_of_day: int
    day_of_week: int
    is_weekend: bool
    is_holiday: bool
    predicted_occupancy_rate: float


class PredictDayResponse(BaseModel):
    date: date_type
    day_of_week: int
    is_weekend: bool
    is_holiday: bool
    hourly_forecast: List[HourlyPrediction]
