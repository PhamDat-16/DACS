from pathlib import Path
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers import (
    auth,
    users,
    lots,
    bookings,
    sessions,
    vehicles,
    navigate,
    predict,
    analytics,
    websocket,
    dynamic_pricing,
)

app = FastAPI(
    title="Smart Parking System API",
    description="API cho hệ thống quản lý bãi đỗ xe thông minh (A* + ML dự báo lấp đầy)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_ORIGIN,
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path == "/" or path.endswith(".html") or path.endswith(".js"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(lots.router)
app.include_router(bookings.router)
app.include_router(sessions.router)
app.include_router(vehicles.router)
app.include_router(navigate.router)
app.include_router(predict.router)
app.include_router(analytics.router)
app.include_router(websocket.router)
app.include_router(dynamic_pricing.router)


@app.get("/api/health", tags=["health"])
def health_check():
    """Dùng để kiểm tra nhanh server có sống không, và test CI/CD sau này."""
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    svg_favicon = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='25' fill='%2310b981'/><text x='50%' y='55%' dominant-baseline='central' text-anchor='middle' font-size='60' font-family='sans-serif' font-weight='900' fill='white'>P</text></svg>"""
    return Response(content=svg_favicon, media_type="image/svg+xml")


from fastapi.responses import FileResponse

# Tích hợp phục vụ Frontend trực tiếp từ FastAPI server
frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
if frontend_dir.exists():
    @app.get("/", include_in_schema=False)
    def serve_index():
        index_file = frontend_dir / "index.html"
        return FileResponse(
            str(index_file),
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )

    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")