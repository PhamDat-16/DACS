import json
import logging
from typing import List, Dict, Any
from fastapi import WebSocket

logger = logging.getLogger("websocket_manager")

class ConnectionManager:
    """Quản lý các kết nối WebSocket realtime hai chiều giữa FastAPI backend và các Frontend clients."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total active: {len(self.active_connections)}")

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message, ensure_ascii=False))
        except Exception as e:
            logger.warning(f"Error sending personal message: {e}")

    async def broadcast(self, event_type: str, data: Dict[str, Any] = None):
        """Phát sóng sự kiện tới tất cả các client đang kết nối."""
        payload = {
            "type": event_type,
            "data": data or {},
            "server_time": json.dumps(str(json.dumps("")), default=str)
        }
        import datetime
        payload["timestamp"] = datetime.datetime.now().strftime("%H:%M:%S")

        msg = json.dumps(payload, ensure_ascii=False)
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(msg)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected.append(connection)

        for dead_conn in disconnected:
            self.disconnect(dead_conn)

ws_manager = ConnectionManager()

