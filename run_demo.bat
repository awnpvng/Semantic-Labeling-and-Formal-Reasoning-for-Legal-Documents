@echo off
REM Script để chạy demo CS229 WSD Project
REM Sử dụng: run_demo.bat

echo ==================================
echo CS229 - WSD Demo Launcher
echo ==================================
echo.

echo Starting demo server...
echo URL: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo ==================================
echo.

python -m uvicorn demo.main:app --reload --port 8000

pause
