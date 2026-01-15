@echo off
echo ========================================
echo   CodeCraft AI - Clean Start
echo ========================================

taskkill /F /IM python.exe 2>nul
timeout /t 1 /nobreak >nul

cd backend
start "CodeCraft Backend" cmd /k "python simple_server.py"

timeout /t 3 /nobreak >nul

start http://localhost:5000/enterprise.html

echo.
echo ========================================
echo   READY! Demo URL:
echo   http://localhost:5000/enterprise.html
echo ========================================