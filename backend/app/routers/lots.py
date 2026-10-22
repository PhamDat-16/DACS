from typing import List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as DbSession

from app.core.database import get_db
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot
from app.schemas.parking_lot import ParkingLotCreate, ParkingLotOut, ParkingLotDetail, CityLotNetworkOut
from app.services.lot_service import create_lot_with_grid

router = APIRouter(prefix="/api/lots", tags=["parking-lots"])


# Dữ liệu hạt nhân chuẩn cho mạng lưới chuỗi bãi đỗ xe đô thị Hà Nội
DEFAULT_CITY_NETWORK = [
    {
        "id": "LOT-HN-01",
        "name": "Bãi Đỗ Xe Vincom Center Bà Triệu",
        "address": "191 Bà Triệu, Phường Lê Đại Hành, Quận Hai Bà Trưng, Hà Nội",
        "district": "Hai Bà Trưng",
        "city": "Hà Nội",
        "latitude": 21.0118,
        "longitude": 105.8505,
        "grid_width": 8,
        "grid_height": 6,
        "total_slots": 48,
        "available_slots": 22,
        "occupancy_rate": 0.54,
        "base_rate": 25000,
        "dynamic_rate": 25000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 1.4,
        "travel_time_min": 6
    },
    {
        "id": "LOT-HN-02",
        "name": "Bãi Xe Tràng Tiền Plaza & Hồ Gươm",
        "address": "24 Hai Bà Trưng, Phường Tràng Tiền, Quận Hoàn Kiếm, Hà Nội",
        "district": "Hoàn Kiếm",
        "city": "Hà Nội",
        "latitude": 21.0245,
        "longitude": 105.8538,
        "grid_width": 8,
        "grid_height": 8,
        "total_slots": 64,
        "available_slots": 6,
        "occupancy_rate": 0.91,
        "base_rate": 30000,
        "dynamic_rate": 45000,
        "tier": "surge",
        "tier_name": "Quá Tải (+50%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 0.5,
        "travel_time_min": 2
    },
    {
        "id": "LOT-HN-03",
        "name": "Bãi Xe Lotte Center Liễu Giai",
        "address": "54 Liễu Giai, Phường Cống Vị, Quận Ba Đình, Hà Nội",
        "district": "Ba Đình",
        "city": "Hà Nội",
        "latitude": 21.0332,
        "longitude": 105.8130,
        "grid_width": 10,
        "grid_height": 6,
        "total_slots": 60,
        "available_slots": 38,
        "occupancy_rate": 0.37,
        "base_rate": 25000,
        "dynamic_rate": 20000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 4.2,
        "travel_time_min": 14
    },
    {
        "id": "LOT-HN-04",
        "name": "Bãi Xe Keangnam Landmark 72",
        "address": "Phạm Hùng, Phường Mễ Trì, Quận Cầu Giấy, Hà Nội",
        "district": "Cầu Giấy",
        "city": "Hà Nội",
        "latitude": 21.0172,
        "longitude": 105.7838,
        "grid_width": 10,
        "grid_height": 7,
        "total_slots": 70,
        "available_slots": 48,
        "occupancy_rate": 0.31,
        "base_rate": 25000,
        "dynamic_rate": 20000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 6.8,
        "travel_time_min": 19
    },
    {
        "id": "LOT-HN-05",
        "name": "Bãi Đỗ Xe Đông Kinh Nghĩa Thục",
        "address": "07 Đinh Tiên Hoàng, Hàng Bạc, Hoàn Kiếm, Hà Nội",
        "district": "Hoàn Kiếm",
        "city": "Hà Nội",
        "latitude": 21.0315,
        "longitude": 105.8525,
        "grid_width": 8,
        "grid_height": 6,
        "total_slots": 48,
        "available_slots": 28,
        "occupancy_rate": 0.42,
        "base_rate": 25000,
        "dynamic_rate": 25000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": False,
        "has_roof": False,
        "status": "active",
        "distance_km": 0.3,
        "travel_time_min": 1
    },
    {
        "id": "LOT-HN-06",
        "name": "Bãi Đỗ Xe Siêu Thị Aeon Mall Hà Đông",
        "address": "Khu đô thị Dương Nội, Phường Dương Nội, Quận Hà Đông, Hà Nội",
        "district": "Hà Đông",
        "city": "Hà Nội",
        "latitude": 20.9832,
        "longitude": 105.7485,
        "grid_width": 10,
        "grid_height": 8,
        "total_slots": 80,
        "available_slots": 46,
        "occupancy_rate": 0.42,
        "base_rate": 20000,
        "dynamic_rate": 20000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 11.2,
        "travel_time_min": 24
    },
    {
        "id": "LOT-HN-07",
        "name": "Bãi Xe Hồ Gươm Plaza & Big C Hà Đông",
        "address": "102 Trần Phú, Phường Mộ Lao, Quận Hà Đông, Hà Nội",
        "district": "Hà Đông",
        "city": "Hà Nội",
        "latitude": 20.9785,
        "longitude": 105.7874,
        "grid_width": 9,
        "grid_height": 7,
        "total_slots": 63,
        "available_slots": 19,
        "occupancy_rate": 0.70,
        "base_rate": 20000,
        "dynamic_rate": 25000,
        "tier": "peak",
        "tier_name": "Cao Điểm (+25%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 9.2,
        "travel_time_min": 20
    },
    {
        "id": "LOT-HN-08",
        "name": "Bãi Đỗ Xe Ga Thường Tín & Chợ Phố",
        "address": "Thị trấn Thường Tín, Huyện Thường Tín, Hà Nội (Quốc Lộ 1A)",
        "district": "Thường Tín",
        "city": "Hà Nội",
        "latitude": 20.8712,
        "longitude": 105.8645,
        "grid_width": 8,
        "grid_height": 6,
        "total_slots": 48,
        "available_slots": 36,
        "occupancy_rate": 0.25,
        "base_rate": 15000,
        "dynamic_rate": 12000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": False,
        "status": "active",
        "distance_km": 18.5,
        "travel_time_min": 32
    },
    {
        "id": "LOT-HN-09",
        "name": "Bãi Xe Lotte Mall Tây Hồ & Thủy Cung",
        "address": "272 Võ Chí Công, Phường Phú Thượng, Quận Tây Hồ, Hà Nội",
        "district": "Tây Hồ",
        "city": "Hà Nội",
        "latitude": 21.0725,
        "longitude": 105.8135,
        "grid_width": 10,
        "grid_height": 8,
        "total_slots": 80,
        "available_slots": 26,
        "occupancy_rate": 0.67,
        "base_rate": 25000,
        "dynamic_rate": 25000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 5.8,
        "travel_time_min": 13
    },
    {
        "id": "LOT-HN-10",
        "name": "Bãi Đỗ Xe Aeon Mall Long Biên",
        "address": "27 Cổ Linh, Phường Long Biên, Quận Long Biên, Hà Nội",
        "district": "Long Biên",
        "city": "Hà Nội",
        "latitude": 21.0268,
        "longitude": 105.9015,
        "grid_width": 10,
        "grid_height": 8,
        "total_slots": 80,
        "available_slots": 35,
        "occupancy_rate": 0.56,
        "base_rate": 20000,
        "dynamic_rate": 20000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 6.2,
        "travel_time_min": 15
    },
    {
        "id": "LOT-HN-11",
        "name": "Bãi Đỗ Xe Vinhomes Royal City",
        "address": "72A Nguyễn Trãi, Phường Thượng Đình, Quận Thanh Xuân, Hà Nội",
        "district": "Thanh Xuân",
        "city": "Hà Nội",
        "latitude": 21.0028,
        "longitude": 105.8152,
        "grid_width": 10,
        "grid_height": 8,
        "total_slots": 80,
        "available_slots": 22,
        "occupancy_rate": 0.72,
        "base_rate": 25000,
        "dynamic_rate": 31000,
        "tier": "peak",
        "tier_name": "Cao Điểm (+25%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 4.5,
        "travel_time_min": 12
    },
    {
        "id": "LOT-HN-12",
        "name": "Bãi Đỗ Xe Sân Vận Động Quốc Gia Mỹ Đình",
        "address": "Đường Lê Đức Thọ, Phường Mỹ Đình 1, Quận Nam Từ Liêm, Hà Nội",
        "district": "Nam Từ Liêm",
        "city": "Hà Nội",
        "latitude": 21.0205,
        "longitude": 105.7645,
        "grid_width": 12,
        "grid_height": 10,
        "total_slots": 120,
        "available_slots": 85,
        "occupancy_rate": 0.29,
        "base_rate": 20000,
        "dynamic_rate": 16000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": False,
        "status": "active",
        "distance_km": 8.5,
        "travel_time_min": 22
    },
    {
        "id": "LOT-HN-13",
        "name": "Bãi Xe Vincom Mega Mall Smart City",
        "address": "Đại đô thị Vinhomes Smart City, Tây Mỗ, Quận Nam Từ Liêm, Hà Nội",
        "district": "Nam Từ Liêm",
        "city": "Hà Nội",
        "latitude": 20.9995,
        "longitude": 105.7425,
        "grid_width": 10,
        "grid_height": 10,
        "total_slots": 100,
        "available_slots": 68,
        "occupancy_rate": 0.32,
        "base_rate": 20000,
        "dynamic_rate": 16000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 11.8,
        "travel_time_min": 25
    },
    {
        "id": "LOT-HN-14",
        "name": "Bãi Xe Công Viên Cầu Giấy & Phố Duy Tân",
        "address": "Phố Thành Thái, Phường Dịch Vọng Hậu, Quận Cầu Giấy, Hà Nội",
        "district": "Cầu Giấy",
        "city": "Hà Nội",
        "latitude": 21.0289,
        "longitude": 105.7905,
        "grid_width": 9,
        "grid_height": 7,
        "total_slots": 63,
        "available_slots": 34,
        "occupancy_rate": 0.46,
        "base_rate": 25000,
        "dynamic_rate": 25000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 6.1,
        "travel_time_min": 16
    },
    {
        "id": "LOT-HN-15",
        "name": "Bãi Đỗ Xe Bệnh Viện Bạch Mai & ĐH Bách Khoa",
        "address": "78 Giải Phóng, Phường Phương Mai, Quận Đống Đa, Hà Nội",
        "district": "Đống Đa",
        "city": "Hà Nội",
        "latitude": 21.0035,
        "longitude": 105.8415,
        "grid_width": 9,
        "grid_height": 8,
        "total_slots": 72,
        "available_slots": 14,
        "occupancy_rate": 0.81,
        "base_rate": 25000,
        "dynamic_rate": 31000,
        "tier": "peak",
        "tier_name": "Cao Điểm (+25%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 3.2,
        "travel_time_min": 9
    },
    {
        "id": "LOT-HN-16",
        "name": "Bãi Đỗ Xe Vincom Center Nguyễn Chí Thanh",
        "address": "54A Nguyễn Chí Thanh, Phường Láng Thượng, Quận Đống Đa, Hà Nội",
        "district": "Đống Đa",
        "city": "Hà Nội",
        "latitude": 21.0242,
        "longitude": 105.8118,
        "grid_width": 10,
        "grid_height": 8,
        "total_slots": 80,
        "available_slots": 42,
        "occupancy_rate": 0.47,
        "base_rate": 25000,
        "dynamic_rate": 25000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 4.8,
        "travel_time_min": 14
    },
    {
        "id": "LOT-HN-17",
        "name": "Bãi Xe Hoàng Thành Thăng Long & Lăng Bác",
        "address": "19C Hoàng Diệu, Phường Điện Biên, Quận Ba Đình, Hà Nội",
        "district": "Ba Đình",
        "city": "Hà Nội",
        "latitude": 21.0372,
        "longitude": 105.8402,
        "grid_width": 8,
        "grid_height": 7,
        "total_slots": 56,
        "available_slots": 31,
        "occupancy_rate": 0.45,
        "base_rate": 25000,
        "dynamic_rate": 25000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": False,
        "has_roof": True,
        "status": "active",
        "distance_km": 1.9,
        "travel_time_min": 5
    },
    {
        "id": "LOT-HN-18",
        "name": "Bãi Xe Nhà Ga Metro Văn Quán (Hà Đông)",
        "address": "Đường Trần Phú, Phường Văn Mỗ, Quận Hà Đông, Hà Nội (Ga Tàu Điện)",
        "district": "Hà Đông",
        "city": "Hà Nội",
        "latitude": 20.9740,
        "longitude": 105.7820,
        "grid_width": 8,
        "grid_height": 7,
        "total_slots": 56,
        "available_slots": 38,
        "occupancy_rate": 0.32,
        "base_rate": 15000,
        "dynamic_rate": 12000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 8.7,
        "travel_time_min": 19
    },
    {
        "id": "LOT-HN-19",
        "name": "Bãi Đỗ Xe Bến Xe Nước Ngầm & Pháp Vân",
        "address": "01 Ngọc Hồi, Phường Hoàng Liệt, Quận Hoàng Mai, Hà Nội",
        "district": "Hoàng Mai",
        "city": "Hà Nội",
        "latitude": 20.9655,
        "longitude": 105.8425,
        "grid_width": 10,
        "grid_height": 8,
        "total_slots": 80,
        "available_slots": 50,
        "occupancy_rate": 0.37,
        "base_rate": 20000,
        "dynamic_rate": 20000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": False,
        "status": "active",
        "distance_km": 7.4,
        "travel_time_min": 17
    },
    {
        "id": "LOT-HN-20",
        "name": "Bãi Xe Khu Công Nghiệp Hà Bình Phương",
        "address": "Xã Văn Bình, Huyện Thường Tín, Hà Nội (Cụm KCN Phía Nam)",
        "district": "Thường Tín",
        "city": "Hà Nội",
        "latitude": 20.8850,
        "longitude": 105.8600,
        "grid_width": 8,
        "grid_height": 7,
        "total_slots": 56,
        "available_slots": 42,
        "occupancy_rate": 0.25,
        "base_rate": 15000,
        "dynamic_rate": 12000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 16.8,
        "travel_time_min": 28
    },
    {
        "id": "LOT-HN-21",
        "name": "Bãi Xe Công Viên Nước Hồ Tây & Thung Lũng Hoa",
        "address": "614 Lạc Long Quân, Phường Nhật Tân, Quận Tây Hồ, Hà Nội",
        "district": "Tây Hồ",
        "city": "Hà Nội",
        "latitude": 21.0695,
        "longitude": 105.8210,
        "grid_width": 9,
        "grid_height": 8,
        "total_slots": 72,
        "available_slots": 45,
        "occupancy_rate": 0.37,
        "base_rate": 25000,
        "dynamic_rate": 20000,
        "tier": "off_peak",
        "tier_name": "Tiết Kiệm (-20%)",
        "has_ev": True,
        "has_roof": False,
        "status": "active",
        "distance_km": 5.4,
        "travel_time_min": 12
    },
    {
        "id": "LOT-HN-22",
        "name": "Bãi Đỗ Xe Ga T1-T2 Sân Bay Quốc Tế Nội Bài",
        "address": "Cảng Hàng Không Quốc Tế Nội Bài, Xã Phú Minh, Huyện Sóc Sơn, Hà Nội",
        "district": "Sóc Sơn",
        "city": "Hà Nội",
        "latitude": 21.2187,
        "longitude": 105.8042,
        "grid_width": 12,
        "grid_height": 12,
        "total_slots": 144,
        "available_slots": 78,
        "occupancy_rate": 0.46,
        "base_rate": 20000,
        "dynamic_rate": 20000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 24.5,
        "travel_time_min": 35
    },
    {
        "id": "LOT-HN-DN",
        "name": "Bãi Đỗ Xe KĐT Đô Nghĩa (Hà Đông)",
        "address": "Khu Đô Thị Mới Đô Nghĩa, Phường Yên Nghĩa, Quận Hà Đông, Hà Nội",
        "district": "Hà Đông",
        "city": "Hà Nội",
        "latitude": 20.9485,
        "longitude": 105.7482,
        "grid_width": 10,
        "grid_height": 8,
        "total_slots": 80,
        "available_slots": 45,
        "occupancy_rate": 0.44,
        "base_rate": 15000,
        "dynamic_rate": 15000,
        "tier": "normal",
        "tier_name": "Tiêu Chuẩn (1.0x)",
        "has_ev": True,
        "has_roof": True,
        "status": "active",
        "distance_km": 0.8,
        "travel_time_min": 3
    }
]


@router.get("/city-network", response_model=List[CityLotNetworkOut])
def get_city_lots_network(db: DbSession = Depends(get_db)):
    """Trả về danh sách toàn bộ các bãi đỗ xe trong mạng lưới đô thị kèm tọa độ GIS và trạng thái realtime."""
    db_lots = db.query(ParkingLot).all()
    results = []

    # Map existing DB lots
    for lot in db_lots:
        total = db.query(ParkingSlot).filter(ParkingSlot.lot_id == lot.id, ParkingSlot.is_obstacle.is_(False)).count() or (lot.grid_width * lot.grid_height)
        avail = db.query(ParkingSlot).filter(ParkingSlot.lot_id == lot.id, ParkingSlot.is_obstacle.is_(False), ParkingSlot.status == "available").count() or int(total * 0.6)
        occ = round((total - avail) / total, 2) if total > 0 else 0.4
        
        # Biểu giá động
        rate = lot.hourly_base_rate or 25000
        tier = "normal"
        tier_name = "Tiêu Chuẩn"
        if occ < 0.35:
            rate = int(rate * 0.8)
            tier = "off_peak"
            tier_name = "Tiết Kiệm (-20%)"
        elif occ >= 0.85:
            rate = int(rate * 1.5)
            tier = "surge"
            tier_name = "Quá Tải (+50%)"
        elif occ >= 0.70:
            rate = int(rate * 1.25)
            tier = "peak"
            tier_name = "Cao Điểm (+25%)"

        results.append(CityLotNetworkOut(
            id=str(lot.id),
            name=lot.name,
            address=lot.address or "Hà Nội",
            district=lot.district or "Hoàn Kiếm",
            city=lot.city or "Hà Nội",
            latitude=lot.latitude or 21.0285,
            longitude=lot.longitude or 105.8542,
            grid_width=lot.grid_width,
            grid_height=lot.grid_height,
            total_slots=total,
            available_slots=avail,
            occupancy_rate=occ,
            base_rate=lot.hourly_base_rate or 25000,
            dynamic_rate=rate,
            tier=tier,
            tier_name=tier_name,
            has_ev=lot.has_ev_charging if lot.has_ev_charging is not None else True,
            has_roof=lot.has_roof if lot.has_roof is not None else True,
            status=lot.status or "active",
            distance_km=1.2,
            travel_time_min=5
        ))

    # Nếu DB có ít hơn 3 bãi, bổ sung dữ liệu chuỗi mẫu
    existing_names = {r.name for r in results}
    for item in DEFAULT_CITY_NETWORK:
        if item["name"] not in existing_names:
            results.append(CityLotNetworkOut(**item))

    return results


@router.post("", response_model=ParkingLotOut)
def create_lot(payload: ParkingLotCreate, db: DbSession = Depends(get_db)):
    """Tạo bãi xe mới trong chuỗi đô thị kèm tự động sinh lưới ô đỗ."""
    return create_lot_with_grid(db, payload)


@router.get("", response_model=List[ParkingLotOut])
def list_lots(db: DbSession = Depends(get_db)):
    return db.query(ParkingLot).all()


@router.get("/{lot_id}", response_model=ParkingLotDetail)
def get_lot_detail(lot_id: str, db: DbSession = Depends(get_db)):
    """Trả về chi tiết bãi xe hoặc dữ liệu mẫu nếu là bãi mã giả lập LOT-HN-XX."""
    # Check if UUID
    try:
        u_id = uuid.UUID(lot_id)
        lot = db.query(ParkingLot).filter(ParkingLot.id == u_id).first()
        if lot:
            return lot
    except ValueError:
        pass

    # Nếu là bãi chuỗi mặc định
    for item in DEFAULT_CITY_NETWORK:
        if item["id"] == lot_id:
            # Tạo dummy detail
            slots = []
            for y in range(item["grid_height"]):
                for x in range(item["grid_width"]):
                    # Giả lập vật cản tường giữa bãi
                    is_obs = (x in (2, 5) and y in (2, 3))
                    slots.append({
                        "id": uuid.uuid4(),
                        "slot_code": f"{chr(65 + y)}-{x+1:02d}",
                        "pos_x": x,
                        "pos_y": y,
                        "status": "available" if (x + y) % 3 != 0 else "occupied",
                        "is_obstacle": is_obs
                    })
            return {
                "id": uuid.uuid4(),
                "name": item["name"],
                "address": item["address"],
                "grid_width": item["grid_width"],
                "grid_height": item["grid_height"],
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "district": item["district"],
                "city": item["city"],
                "hourly_base_rate": item["base_rate"],
                "has_ev_charging": item["has_ev"],
                "has_roof": item["has_roof"],
                "status": item["status"],
                "slots": slots
            }

    raise HTTPException(status_code=404, detail="Không tìm thấy bãi xe")


@router.get("/{lot_id}/available-slots")
def count_available_slots(lot_id: str, db: DbSession = Depends(get_db)):
    """Đếm nhanh số slot còn trống."""
    try:
        u_id = uuid.UUID(lot_id)
        total = db.query(ParkingSlot).filter(ParkingSlot.lot_id == u_id, ParkingSlot.is_obstacle.is_(False)).count()
        available = db.query(ParkingSlot).filter(ParkingSlot.lot_id == u_id, ParkingSlot.is_obstacle.is_(False), ParkingSlot.status == "available").count()
        return {"total": total, "available": available}
    except ValueError:
        for item in DEFAULT_CITY_NETWORK:
            if item["id"] == lot_id:
                return {"total": item["total_slots"], "available": item["available_slots"]}
        return {"total": 48, "available": 24}
