@echo off
title Smart Parking System - Fullstack Integrated Server
echo ===================================================
echo     SMART PARKING SYSTEM (A* + ML + GSAP)
echo ===================================================
echo.
echo Dang khoi dong he thong Backend va Frontend tich hop...
echo.

cd /d "%~dp0backend"
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo He thong dang chay tai:
echo   - Giao dien Web Frontend : http://localhost:8000
echo   - Swagger API Docs       : http://localhost:8000/docs
echo   - API Health Check       : http://localhost:8000/api/health
echo.
echo Nhan Ctrl + C de dung server bat cu luc nao.
echo.

uvicorn app.main:app --reload --port 8000
pause

