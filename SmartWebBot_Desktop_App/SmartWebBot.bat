@echo off
title SmartWebBot Desktop App
echo SmartWebBot Desktop App
echo ========================
echo.

cd /d "%~dp0"

echo Starting SmartWebBot...
echo.

python launch_app_simple.py

if errorlevel 1 (
    echo.
    echo Error starting SmartWebBot. Please check the error messages above.
    echo.
    pause
)
