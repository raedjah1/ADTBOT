@echo off
title SmartWebBot - Complete Reinstallation
color 0A
echo.
echo  ╔════════════════════════════════════════╗
echo  ║  SmartWebBot Complete Reinstallation  ║
echo  ╚════════════════════════════════════════╝
echo.

set "INSTALL_DIR=%USERPROFILE%\Desktop\SmartWebBot"

echo [INFO] Reinstalling SmartWebBot with complete frontend...
echo Installation directory: %INSTALL_DIR%
echo.

echo [1/5] Removing old installation...
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"

echo [2/5] Copying application files...
xcopy /E /I /H /Y "smartwebbot" "%INSTALL_DIR%\smartwebbot\"
xcopy /E /I /H /Y "frontend" "%INSTALL_DIR%\frontend\"
xcopy /E /I /H /Y "config" "%INSTALL_DIR%\config\"
copy /Y "backend_server.py" "%INSTALL_DIR%\"
copy /Y "config.yaml" "%INSTALL_DIR%\"
copy /Y "requirements.txt" "%INSTALL_DIR%\"

echo [3/5] Copying launcher scripts...
copy /Y "C:\Users\Raed.Jah\Desktop\SmartWebBot_Copy\SmartWebBot_Desktop_App\SmartWebBot_Full.bat" "%INSTALL_DIR%\SmartWebBot.bat" 2>nul
if not exist "%INSTALL_DIR%\SmartWebBot.bat" (
    echo Creating new launcher...
    echo @echo off > "%INSTALL_DIR%\SmartWebBot.bat"
    echo title SmartWebBot Desktop App >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo cd /d "%%~dp0" >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo echo Starting SmartWebBot... >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo taskkill /F /IM python.exe /FI "WINDOWTITLE eq *backend*" ^>nul 2^>^&1 >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo taskkill /F /IM node.exe ^>nul 2^>^&1 >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo start /B "SmartWebBot Backend" python backend_server.py >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo timeout /t 5 /nobreak ^>nul >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo cd frontend >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo start "SmartWebBot Frontend" cmd /k "npm start" >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo timeout /t 10 /nobreak ^>nul >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo echo SmartWebBot is running! >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo echo Frontend: http://localhost:3000 >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo echo Backend: http://localhost:8000 >> "%INSTALL_DIR%\SmartWebBot.bat"
    echo pause >> "%INSTALL_DIR%\SmartWebBot.bat"
)

echo [4/5] Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\SmartWebBot.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\SmartWebBot.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'SmartWebBot Desktop App'; $Shortcut.Save()"

echo [5/5] Verifying installation...
if exist "%INSTALL_DIR%\frontend\package.json" (
    echo [OK] Frontend installed successfully
) else (
    echo [ERROR] Frontend not found - please check the installation
)

if exist "%INSTALL_DIR%\backend_server.py" (
    echo [OK] Backend installed successfully
) else (
    echo [ERROR] Backend not found - please check the installation
)

echo.
echo ╔════════════════════════════════════════╗
echo ║  Installation Complete!               ║
echo ╚════════════════════════════════════════╝
echo.
echo SmartWebBot has been installed to: %INSTALL_DIR%
echo Desktop shortcut created: SmartWebBot
echo.
echo To run SmartWebBot:
echo 1. Double-click the "SmartWebBot" shortcut on your desktop
echo 2. Wait for both backend and frontend to start
echo 3. Your browser will open automatically at http://localhost:3000
echo.
pause
