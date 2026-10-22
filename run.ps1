# Smart Parking System - Fullstack Integrated Launcher
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "    SMART PARKING SYSTEM (A* + ML + GSAP)" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dang khoi dong he thong Backend va Frontend tich hop..." -ForegroundColor Green
Write-Host ""

$backendDir = Join-Path $PSScriptRoot "backend"
$venvPython = Join-Path $backendDir "venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    Write-Host "-> Da tim thay virtualenv tai: $venvPython" -ForegroundColor Gray
} else {
    Write-Host "-> Dang su dung python he thong..." -ForegroundColor Gray
    $venvPython = "python"
}

Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  * Giao dien Web Frontend : http://localhost:8000" -ForegroundColor Green
Write-Host "  * Swagger API Docs       : http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "  * API Health Check       : http://localhost:8000/api/health" -ForegroundColor White
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Nhan Ctrl + C de dung he thong.`n" -ForegroundColor DarkGray

& $venvPython -m uvicorn app.main:app --reload --port 8000 --app-dir $backendDir

