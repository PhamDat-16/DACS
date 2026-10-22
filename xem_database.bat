@echo off
chcp 65001 >nul
echo Dang ket noi co so du lieu PostgreSQL...
backend\venv\Scripts\python.exe view_db.py
pause

