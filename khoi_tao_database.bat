@echo off
chcp 65001 >nul
title KHOI TAO CO SO DU LIEU SMART PARKING SYSTEM

echo =====================================================================
echo       NHAP VA KHOI TAO CSDL POSTGRESQL (smart_parking_backup.sql)
echo =====================================================================
echo.
echo Script nay se tao database 'parking_system' va nap 6 bang du lieu mau cua do an.
echo.

set /p PG_USER="Nhap ten PostgreSQL user [mac dinh: postgres]: "
if "%PG_USER%"=="" set PG_USER=postgres

set /p PG_PORT="Nhap cong PostgreSQL port [mac dinh: 5432]: "
if "%PG_PORT%"=="" set PG_PORT=5432

echo.
echo [*] Dang kiem tra va tao Database 'parking_system'...
psql -U %PG_USER% -p %PG_PORT% -c "CREATE DATABASE parking_system;" 2>nul
if %errorlevel% equ 0 (
    echo [+] Da tao thanh cong database 'parking_system'!
) else (
    echo [i] Database 'parking_system' co the da ton tai, tiep tuc nap du lieu...
)

echo.
echo [*] Dang nap du lieu tu smart_parking_backup.sql vao parking_system...
echo (Neu PostgreSQL yeu cau mat khau, vui long nhap mat khau vao console)
psql -U %PG_USER% -p %PG_PORT% -d parking_system -f "%~dp0smart_parking_backup.sql"

if %errorlevel% equ 0 (
    echo.
    echo =====================================================================
    echo   [OK] NAP DU LIEU DATABASE THANH CONG 100%!
    echo   Ban co the chay 'xem_database.bat' de kiem tra hoac 'run_web.bat' de dung web.
    echo =====================================================================
) else (
    echo.
    echo [!] Luu y neu gap loi chua co psql trong PATH:
    echo     Ban co the mo pgAdmin 4 -> nhap chuot phai Databases -> Create Database 'parking_system'
    echo     -> nhap chuot phai vao 'parking_system' -> Restore -> chon file smart_parking_backup.sql!
)
echo.
pause
