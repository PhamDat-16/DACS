from datetime import date as date_type, datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.ml_engine.predict import predict_occupancy, predict_full_day

router = APIRouter(prefix="/api/dynamic-pricing", tags=["dynamic-pricing"])

class DynamicPricingConfig(BaseModel):
    base_rate_hourly: int = 25000
    offpeak_discount: float = 0.20  # Giảm 20% khi lấp đầy < 35%
    peak_surcharge: float = 0.25    # Tăng 25% khi lấp đầy 70% - 85%
    surge_surcharge: float = 0.50   # Tăng 50% khi lấp đầy > 85%
    low_threshold: float = 0.35
    high_threshold: float = 0.70
    surge_threshold: float = 0.85

_PRICING_CONFIG = DynamicPricingConfig()

def calculate_dynamic_rate(occupancy_rate: float, config: DynamicPricingConfig) -> Dict[str, Any]:
    base = config.base_rate_hourly
    if occupancy_rate < config.low_threshold:
        multiplier = 1.0 - config.offpeak_discount
        tier = "off_peak"
        tier_name = "Giờ Thấp Điểm (Tiết Kiệm)"
        badge_color = "emerald"
        discount_percent = int(config.offpeak_discount * 100)
        badge_text = f"🏷️ Giảm {discount_percent}%"
    elif occupancy_rate <= config.high_threshold:
        multiplier = 1.0
        tier = "normal"
        tier_name = "Giờ Tiêu Chuẩn"
        badge_color = "cyan"
        badge_text = "Tiêu Chuẩn"
    elif occupancy_rate <= config.surge_threshold:
        multiplier = 1.0 + config.peak_surcharge
        tier = "peak"
        tier_name = "Giờ Cao Điểm"
        badge_color = "amber"
        surcharge_percent = int(config.peak_surcharge * 100)
        badge_text = f"🔥 Tăng {surcharge_percent}%"
    else:
        multiplier = 1.0 + config.surge_surcharge
        tier = "surge"
        tier_name = "Giờ Đặc Biệt Đông (Surge)"
        badge_color = "rose"
        surcharge_percent = int(config.surge_surcharge * 100)
        badge_text = f"⚡ Tăng {surcharge_percent}%"

    final_rate = int(round(base * multiplier / 1000.0) * 1000)
    return {
        "base_rate": base,
        "final_rate": final_rate,
        "multiplier": round(multiplier, 2),
        "tier": tier,
        "tier_name": tier_name,
        "badge_color": badge_color,
        "badge_text": badge_text,
        "occupancy_rate": round(occupancy_rate, 2),
        "savings_or_extra": final_rate - base
    }

@router.get("/current")
def get_current_pricing():
    """Lấy biểu phí động áp dụng cho giờ hiện tại."""
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    is_weekend = day_of_week >= 5

    try:
        occupancy = predict_occupancy(hour, day_of_week, is_weekend, False)
    except Exception:
        occupancy = 0.45

    pricing = calculate_dynamic_rate(occupancy, _PRICING_CONFIG)
    return {
        "current_hour": hour,
        "time_str": now.strftime("%H:%M"),
        "date_str": now.strftime("%d/%m/%Y"),
        "is_weekend": is_weekend,
        **pricing
    }

@router.get("/24h")
def get_24h_dynamic_pricing(
    date: Optional[date_type] = Query(None, description="Ngày dự báo (YYYY-MM-DD)")
):
    """Tính toán ma trận giá linh hoạt cho toàn bộ 24 giờ trong ngày."""
    target_date = date or datetime.now().date()
    day_of_week = target_date.weekday()
    is_weekend = day_of_week >= 5

    try:
        hourly_forecast = predict_full_day(day_of_week, is_weekend, False)
    except Exception:
        hourly_forecast = [{"hour_of_day": h, "predicted_occupancy_rate": 0.45} for h in range(24)]

    matrix = []
    for item in hourly_forecast:
        h = item["hour_of_day"]
        occ = item["predicted_occupancy_rate"]
        pr = calculate_dynamic_rate(occ, _PRICING_CONFIG)
        matrix.append({
            "hour": h,
            "hour_label": f"{h:02d}:00",
            **pr
        })

    return {
        "date": str(target_date),
        "is_weekend": is_weekend,
        "base_rate": _PRICING_CONFIG.base_rate_hourly,
        "hourly_pricing": matrix
    }

@router.get("/ai-recommendations")
def get_ai_parking_recommendations(
    date: Optional[date_type] = Query(None, description="Ngày cần gợi ý")
):
    """Trợ lý AI phân tích và đưa ra khuyến nghị thời điểm đỗ xe tối ưu nhất."""
    target_date = date or datetime.now().date()
    day_of_week = target_date.weekday()
    is_weekend = day_of_week >= 5

    try:
        hourly_forecast = predict_full_day(day_of_week, is_weekend, False)
    except Exception:
        hourly_forecast = [{"hour_of_day": h, "predicted_occupancy_rate": 0.45} for h in range(24)]

    # Sắp xếp để tìm các giờ có tỷ lệ lấp đầy thấp nhất (rẻ nhất & trống nhất)
    # Loại trừ ban đêm 0h-5h nếu người dùng gửi ban ngày
    daytime_hours = [item for item in hourly_forecast if 6 <= item["hour_of_day"] <= 22]
    daytime_sorted = sorted(daytime_hours, key=lambda x: x["predicted_occupancy_rate"])

    best_hours = []
    for item in daytime_sorted[:3]:
        h = item["hour_of_day"]
        occ = item["predicted_occupancy_rate"]
        pr = calculate_dynamic_rate(occ, _PRICING_CONFIG)
        best_hours.append({
            "hour": h,
            "time_range": f"{h:02d}:00 - {h+1:02d}:00",
            "occupancy_percent": int(round(occ * 100)),
            "price": pr["final_rate"],
            "discount_text": pr["badge_text"],
            "recommendation_reason": "Nhiều ô trống nhất, giá vé rẻ nhất trong ngày."
        })

    # Tìm các giờ cao điểm tắc nghẽn cần tránh
    peak_hours = []
    for item in sorted(daytime_hours, key=lambda x: x["predicted_occupancy_rate"], reverse=True)[:2]:
        h = item["hour_of_day"]
        occ = item["predicted_occupancy_rate"]
        pr = calculate_dynamic_rate(occ, _PRICING_CONFIG)
        peak_hours.append({
            "hour": h,
            "time_range": f"{h:02d}:00 - {h+1:02d}:00",
            "occupancy_percent": int(round(occ * 100)),
            "price": pr["final_rate"],
            "warning": "Lưu lượng xe cao điểm, nguy cơ hết chỗ và phí phụ thu cao."
        })

    return {
        "date": str(target_date),
        "best_value_hours": best_hours,
        "peak_avoid_hours": peak_hours,
        "max_savings_percent": int(_PRICING_CONFIG.offpeak_discount * 100),
        "ai_summary": f"Trợ lý AI khuyên bạn nên đỗ xe vào khung giờ {best_hours[0]['time_range']} để được giảm {int(_PRICING_CONFIG.offpeak_discount*100)}% cước phí và dễ dàng tìm ô đỗ đẹp gần cổng!"
    }

@router.post("/config")
def update_dynamic_pricing_config(config: DynamicPricingConfig):
    """Cập nhật cấu hình định giá động (Dành cho Quản trị viên)."""
    global _PRICING_CONFIG
    _PRICING_CONFIG = config
    return {"status": "success", "config": _PRICING_CONFIG}
