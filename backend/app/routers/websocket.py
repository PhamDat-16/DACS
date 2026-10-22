import asyncio
import datetime
import json
import random
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel

from app.core.websocket_manager import ws_manager

router = APIRouter(tags=["realtime-websocket"])

class BroadcastPayload(BaseModel):
    event_type: str
    data: Dict[str, Any] = {}

class IoTEventSimulation(BaseModel):
    sensor_id: str
    slot_code: str
    is_occupied: bool
    distance_cm: Optional[int] = None
    battery_level: Optional[int] = None

# Sinh dữ liệu Telemetry cho 48 ô đỗ (6 hàng x 8 cột)
def get_sensor_telemetry_dataset() -> List[Dict[str, Any]]:
    rows = ["A", "B", "C", "D", "E", "F"]
    sensors = []
    
    # Một vài ô mẫu có trạng thái đặc biệt
    occupied_slots = {"A-01", "A-04", "B-02", "C-05", "D-03", "E-06", "F-02"}
    low_battery_slots = {"B-05", "D-06"}
    
    for r_idx, row in enumerate(rows):
        for col in range(1, 9):
            code = f"{row}-{col:02d}"
            sensor_id = f"SNS-{row}{col:02d}"
            is_occ = code in occupied_slots
            is_low_bat = code in low_battery_slots
            
            # Nếu có xe thì khoảng cách phản xạ siêu âm ngắn (15 - 45 cm)
            # Nếu trống thì khoảng cách lớn (190 - 240 cm)
            distance = random.randint(18, 38) if is_occ else random.randint(205, 235)
            battery = random.randint(12, 19) if is_low_bat else random.randint(75, 98)
            rssi = random.randint(-75, -55) # dBm
            
            sensors.append({
                "sensor_id": sensor_id,
                "slot_code": code,
                "sensor_type": "Ultrasonic Dual-Echo + Magnetic",
                "distance_cm": distance,
                "is_occupied": is_occ,
                "battery_level": battery,
                "rssi_dbm": rssi,
                "signal_quality": "Tuyệt vời" if rssi > -65 else "Tốt" if rssi > -80 else "Yếu",
                "temperature_c": round(28.5 + random.uniform(-1.5, 2.5), 1),
                "firmware": "v2.4.1-Mesh",
                "status": "warning" if battery < 20 else "online",
                "last_heartbeat": (datetime.datetime.now() - datetime.timedelta(seconds=random.randint(1, 45))).strftime("%H:%M:%S")
            })
    return sensors

_IOT_SENSORS_CACHE = get_sensor_telemetry_dataset()

@router.websocket("/ws/realtime")
async def websocket_realtime_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint chính kết nối Full-Duplex giữa Frontend và Backend.
    Hỗ trợ Ping-Pong đo latency, broadcast cập nhật ô đỗ, trạng thái barrier và telemetry IoT.
    """
    await ws_manager.connect(websocket)
    try:
        # Gửi thông điệp chào mừng Handshake ban đầu
        await ws_manager.send_personal_message(
            {
                "type": "INIT",
                "message": "Connected to Smart Parking Realtime WebSocket Hub",
                "active_connections": len(ws_manager.active_connections),
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
            },
            websocket
        )

        while True:
            raw_text = await websocket.receive_text()
            try:
                msg = json.loads(raw_text)
                msg_type = msg.get("type", "")

                if msg_type == "ping":
                    # Phản hồi Pong kèm timestamp client để tính RTT latency
                    await ws_manager.send_personal_message(
                        {
                            "type": "pong",
                            "client_time": msg.get("client_time", 0),
                            "server_time": datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                        },
                        websocket
                    )

                elif msg_type == "broadcast":
                    # Client kích hoạt broadcast (ví dụ: thông báo khẩn cấp từ admin)
                    event_type = msg.get("event_type", "GENERIC_EVENT")
                    event_data = msg.get("data", {})
                    await ws_manager.broadcast(event_type, event_data)

                elif msg_type == "simulate_traffic":
                    # Kích hoạt sự kiện giao thông
                    await ws_manager.broadcast("TRAFFIC_EVENT", msg.get("data", {}))

            except json.JSONDecodeError:
                pass

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        ws_manager.disconnect(websocket)


@router.post("/api/realtime/broadcast")
async def api_broadcast_event(payload: BroadcastPayload):
    """API REST để kích hoạt broadcast WebSocket từ các module backend khác."""
    await ws_manager.broadcast(payload.event_type, payload.data)
    return {
        "status": "success",
        "broadcasted_to": len(ws_manager.active_connections),
        "event_type": payload.event_type
    }


@router.get("/api/realtime/iot-telemetry")
def get_iot_telemetry():
    """Lấy dữ liệu telemetry danh sách cảm biến IoT bãi xe."""
    global _IOT_SENSORS_CACHE
    # Cập nhật nhẹ thời gian heartbeat và nhiệt độ cho sống động
    for s in _IOT_SENSORS_CACHE:
        s["temperature_c"] = round(28.5 + random.uniform(-1.0, 2.0), 1)
        s["last_heartbeat"] = datetime.datetime.now().strftime("%H:%M:%S")
    return {
        "total_sensors": len(_IOT_SENSORS_CACHE),
        "online_count": sum(1 for s in _IOT_SENSORS_CACHE if s["status"] == "online"),
        "warning_count": sum(1 for s in _IOT_SENSORS_CACHE if s["status"] == "warning"),
        "occupied_count": sum(1 for s in _IOT_SENSORS_CACHE if s["is_occupied"]),
        "sensors": _IOT_SENSORS_CACHE
    }


@router.post("/api/realtime/simulate-iot-event")
async def simulate_iot_event(payload: IoTEventSimulation):
    """Giả lập sự kiện cảm biến phát hiện xe đỗ vào hoặc xe rời đi."""
    global _IOT_SENSORS_CACHE
    target = next((s for s in _IOT_SENSORS_CACHE if s["sensor_id"] == payload.sensor_id or s["slot_code"] == payload.slot_code), None)
    
    if target:
        target["is_occupied"] = payload.is_occupied
        if payload.distance_cm is not None:
            target["distance_cm"] = payload.distance_cm
        else:
            target["distance_cm"] = random.randint(18, 35) if payload.is_occupied else random.randint(210, 230)
        
        if payload.battery_level is not None:
            target["battery_level"] = payload.battery_level
            target["status"] = "warning" if payload.battery_level < 20 else "online"

        target["last_heartbeat"] = datetime.datetime.now().strftime("%H:%M:%S")

        # Broadcast sự kiện WebSocket tới tất cả các clients
        await ws_manager.broadcast("IOT_SENSOR_TRIGGERED", {
            "sensor": target,
            "slot_code": target["slot_code"],
            "is_occupied": target["is_occupied"],
            "distance_cm": target["distance_cm"]
        })

        return {"status": "success", "sensor": target}

    raise HTTPException(status_code=404, detail="Không tìm thấy cảm biến")

