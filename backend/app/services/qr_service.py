import base64
import io
import uuid

import qrcode


def generate_booking_token() -> str:
    """Token duy nhất định danh cho 1 booking - nhúng vào mã QR."""
    return f"BOOKING-{uuid.uuid4().hex}"


def generate_qr_base64(data: str) -> str:
    """
    Sinh ảnh QR code (PNG) từ chuỗi dữ liệu, trả về dạng base64 data-URI
    để frontend có thể hiển thị trực tiếp bằng thẻ <img src="...">
    mà không cần lưu file ảnh riêng trên server.
    """
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
