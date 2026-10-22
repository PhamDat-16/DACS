@echo off
chcp 65001 >nul
title KHOI DONG HE THONG SMART PARKING SYSTEM

echo =====================================================================
echo       DANG KHOI DONG HE THONG SMART PARKING SYSTEM (SPS)
echo =====================================================================
echo.

:: 1. Bat Backend FastAPI tren cong 8000
echo [1/2] Dang khoi dong Backend FastAPI tai http://127.0.0.1:8000...
start "SPS - Backend FastAPI (Port 8000)" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

:: Doi 2 giay cho Backend on dinh
timeout /t 2 /nobreak >nul

:: 2. Bat Frontend Web Server tren cong 3000
echo [2/2] Dang khoi dong Frontend tai http://localhost:3000...
start "SPS - Frontend Web (Port 3000)" cmd /k "cd /d %~dp0frontend && ..\backend\venv\Scripts\python.exe -m http.server 3000"

:: Doi 1 giay roi tu dong mo trinh duyet
timeout /t 1 /nobreak >nul
echo.
echo -> Dang tu dong mo trinh duyet Web...
start http://localhost:3000

echo.
echo =====================================================================
echo   DA KHOI DONG THANH CONG!
echo   - Giao dien Web:        http://localhost:3000
echo   - API Swagger Docs:     http://127.0.0.1:8000/docs
echo =====================================================================
echo (Khong tat 2 cua so den vua hien len de giu he thong hoat dong)
echo.
pause

