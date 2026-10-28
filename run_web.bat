@echo off
chcp 65001 >nul
title KHOI DONG HE THONG SMART PARKING SYSTEM

echo =====================================================================
echo       DANG KHOI DONG HE THONG SMART PARKING SYSTEM (SPS)
echo =====================================================================
echo.

:: 0. Kiem tra va tu dong tao file .env neu chua co
if not exist "%~dp0.env" (
    if exist "%~dp0.env.example" (
        echo [*] Phat hien chua co file .env, dang tu dong khoi tao tu .env.example...
        copy "%~dp0.env.example" "%~dp0.env" >nul
        echo [+] Da tao xong file .env!
    )
)

:: 1. Kiem tra moi truong ao Python venv, neu chua co thi tu dong cai dat
if not exist "%~dp0backend\venv\Scripts\python.exe" (
    echo =====================================================================
    echo [THONG BAO] Chua tim thay thu vien Python trong backend\venv!
    echo He thong dang tu dong tao moi truong ao va cai dat thu vien tu requirements.txt...
    echo (Qua trinh nay chi dien ra 1 lan duy nhat luc khoi dong lan dau, mat 1-2 phut)
    echo =====================================================================
    echo.
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [LOI] May tinh cua ban chua cai dat Python hoac chua tick 'Add Python to PATH'!
        echo Vui long cai dat Python 3.10 hoac 3.11 tai https://www.python.org roi chay lai script nay.
        echo.
        pause
        exit /b 1
    )
    echo [*] Dang tao moi truong ao Python venv tai backend\venv...
    python -m venv "%~dp0backend\venv"
    echo [*] Dang cai dat cac thu vien can thiet (FastAPI, SQLAlchemy, scikit-learn...)...
    "%~dp0backend\venv\Scripts\python.exe" -m pip install --upgrade pip -q
    "%~dp0backend\venv\Scripts\pip.exe" install -r "%~dp0backend\requirements.txt"
    echo.
    echo [+] Cai dat moi truong hoan tat! Tiep tuc khoi dong he thong...
    echo.
)

:: 2. Bat Backend FastAPI tren cong 8000
echo [1/2] Dang khoi dong Backend FastAPI tai http://127.0.0.1:8000...
start "SPS - Backend FastAPI (Port 8000)" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

:: Doi 2 giay cho Backend on dinh
timeout /t 2 /nobreak >nul

:: 3. Bat Frontend Web Server tren cong 3000
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
