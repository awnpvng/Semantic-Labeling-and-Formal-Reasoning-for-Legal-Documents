#!/usr/bin/env pwsh
# Script để chạy demo CS229 WSD Project
# Sử dụng: .\run_demo.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "CS229 - WSD Demo Launcher" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra xem đã cài đặt dependencies chưa
Write-Host "Checking dependencies..." -ForegroundColor Yellow

# Kiểm tra fastapi
$fastapi_installed = python -c "import fastapi" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "FastAPI not found. Installing dependencies..." -ForegroundColor Red
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install dependencies. Please check your Python installation." -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "Dependencies OK!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting demo server..." -ForegroundColor Yellow
Write-Host "URL: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Chạy server
python -m uvicorn demo.main:app --reload --port 8000
