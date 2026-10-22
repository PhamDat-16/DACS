import uuid

from sqlalchemy import Column, Integer, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class OccupancyHistory(Base):
    """
    Log tỷ lệ lấp đầy bãi xe theo thời gian - đây là dữ liệu TRAIN cho model ML
    ở Phase 4. Các cột hour_of_day/day_of_week/is_weekend/is_holiday đã ở dạng
    feature sẵn sàng đưa vào model, không cần transform nhiều.
    """

    __tablename__ = "occupancy_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lot_id = Column(UUID(as_uuid=True), ForeignKey("parking_lots.id"), nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    hour_of_day = Column(Integer, nullable=False)      # 0-23
    day_of_week = Column(Integer, nullable=False)       # 0=Monday ... 6=Sunday
    is_weekend = Column(Boolean, nullable=False, default=False)
    is_holiday = Column(Boolean, nullable=False, default=False)
    occupancy_rate = Column(Float, nullable=False)      # 0.0 - 1.0

    lot = relationship("ParkingLot", back_populates="occupancy_logs")
