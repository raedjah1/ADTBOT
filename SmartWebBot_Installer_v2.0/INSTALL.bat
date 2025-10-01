@echo off
title SmartWebBot Installer
color 0A

 ╔════════════════════════════════════════╗
 ║     SmartWebBot Desktop App v2.0      ║
 ║     One-Click Installer               ║
 ╚════════════════════════════════════════╝

[INFO] Welcome to SmartWebBot Installer

This installer will set up SmartWebBot on your computer.

Prerequisites Check:

[1/2] Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
python --version
echo [OK] Python found

[2/2] Checking Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js from:
    echo https://nodejs.org/
    echo.
    echo Download the LTS version and install with default settings.
    pause
    exit /b 1
)
node --version
echo [OK] Node.js found

echo ========================================
echo Installing SmartWebBot...
echo ========================================

set "INSTALL_DIR=%USERPROFILE%\Desktop\SmartWebBot"

echo [1/4] Creating installation directory...
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"

echo [2/4] Copying application files...
xcopy /E /I /H /Y "app\*" "%INSTALL_DIR%\"

echo [3/4] Installing Python dependencies...
cd "%INSTALL_DIR%"
python -m pip install -r requirements.txt --quiet

echo [4/4] Creating desktop shortcut...
cd /d "%~dp0"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut^('%USERPROFILE%\Desktop\SmartWebBot.lnk'^); $Shortcut.TargetPath = '%INSTALL_DIR%\SmartWebBot.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'SmartWebBot Desktop App'; $Shortcut.Save^(^)"

echo Creating launcher...
(
echo @echo off
echo title SmartWebBot
echo cd /d "%%~dp0"
echo taskkill /F /IM python.exe /FI "WINDOWTITLE eq *backend*" ^>nul 2^>^&1
echo taskkill /F /IM node.exe ^>nul 2^>^&1
echo start /B "SmartWebBot Backend" python backend_server.py
echo timeout /t 5 /nobreak ^>nul
echo cd frontend
echo start "SmartWebBot Frontend" cmd /k "npm start"
echo echo SmartWebBot is starting...
echo pause
) > "%INSTALL_DIR%\SmartWebBot.bat"

echo.
echo ╔════════════════════════════════════════╗
echo ║  Installation Complete!               ║
echo ╚════════════════════════════════════════╝
echo.
echo SmartWebBot has been installed successfully!
echo.
echo Installation location: %INSTALL_DIR%
echo Desktop shortcut: SmartWebBot
echo.
echo To run SmartWebBot:
echo 1. Double-click the "SmartWebBot" shortcut on your desktop
echo 2. Wait for the app to start
echo 3. Your browser will open automatically
echo.
pause
