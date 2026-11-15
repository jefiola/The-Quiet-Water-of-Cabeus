@echo off
title The Quiet Water of Cabeus - Launcher
echo Starting backend server...
echo.
echo Opening http://localhost:8000 in browser...
echo.

REM Start backend in background
start "Cabeus Backend" cmd /k "cd /d "%~dp0" && .venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"

REM Wait a moment for server to start
timeout /t 3 >nul

REM Open in default browser
start "" "http://localhost:8000/"

echo.
echo Backend running at http://localhost:8000
echo API docs at http://localhost:8000/api
echo Events at http://localhost:8000/api/events
echo.
echo Press any key to stop server and exit...
pause >nul

REM Kill the backend process
taskkill /f /fi "WINDOWTITLE eq Cabeus Backend" >nul 2>&1