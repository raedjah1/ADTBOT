@echo off
title SmartWebBot - Create Distributable Package
color 0A
echo.
echo  ╔════════════════════════════════════════╗
echo  ║  SmartWebBot Distributable Package    ║
echo  ║  Creator                               ║
echo  ╚════════════════════════════════════════╝
echo.

set "PACKAGE_NAME=SmartWebBot_Installer_v2.0"
set "PACKAGE_DIR=%CD%\%PACKAGE_NAME%"

echo [INFO] Creating distributable package...
echo This will create a package that anyone can install without prerequisites.
echo.

echo [1/6] Creating package structure...
if exist "%PACKAGE_DIR%" (
    rmdir /s /q "%PACKAGE_DIR%"
)
mkdir "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%\app"

echo [2/6] Copying application files...
xcopy /E /I /H /Y "smartwebbot" "%PACKAGE_DIR%\app\smartwebbot\"
xcopy /E /I /H /Y "frontend" "%PACKAGE_DIR%\app\frontend\"
xcopy /E /I /H /Y "config" "%PACKAGE_DIR%\app\config\"
copy /Y "backend_server.py" "%PACKAGE_DIR%\app\"
copy /Y "config.yaml" "%PACKAGE_DIR%\app\"
copy /Y "requirements.txt" "%PACKAGE_DIR%\app\"

echo [3/6] Creating installer script...
(
echo @echo off
echo title SmartWebBot Installer
echo color 0A
echo.
echo  ╔════════════════════════════════════════╗
echo  ║     SmartWebBot Desktop App v2.0      ║
echo  ║     One-Click Installer               ║
echo  ╚════════════════════════════════════════╝
echo.
echo [INFO] Welcome to SmartWebBot Installer
echo.
echo This installer will set up SmartWebBot on your computer.
echo.
echo Prerequisites Check:
echo.
echo [1/2] Checking Python...
echo where python ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo [ERROR] Python not found. Please install Python 3.8+ from:
echo     echo https://www.python.org/downloads/
echo     echo.
echo     echo Make sure to check "Add Python to PATH" during installation.
echo     pause
echo     exit /b 1
echo ^)
echo python --version
echo echo [OK] Python found
echo.
echo [2/2] Checking Node.js...
echo where node ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo [ERROR] Node.js not found. Please install Node.js from:
echo     echo https://nodejs.org/
echo     echo.
echo     echo Download the LTS version and install with default settings.
echo     pause
echo     exit /b 1
echo ^)
echo node --version
echo echo [OK] Node.js found
echo.
echo echo ========================================
echo echo Installing SmartWebBot...
echo echo ========================================
echo.
echo set "INSTALL_DIR=%%USERPROFILE%%\Desktop\SmartWebBot"
echo.
echo echo [1/4] Creating installation directory...
echo if exist "%%INSTALL_DIR%%" ^(
echo     rmdir /s /q "%%INSTALL_DIR%%"
echo ^)
echo mkdir "%%INSTALL_DIR%%"
echo.
echo echo [2/4] Copying application files...
echo xcopy /E /I /H /Y "app\*" "%%INSTALL_DIR%%\"
echo.
echo echo [3/4] Installing Python dependencies...
echo cd "%%INSTALL_DIR%%"
echo python -m pip install -r requirements.txt --quiet
echo.
echo echo [4/4] Creating desktop shortcut...
echo cd /d "%%~dp0"
echo powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut^('%%USERPROFILE%%\Desktop\SmartWebBot.lnk'^); $Shortcut.TargetPath = '%%INSTALL_DIR%%\SmartWebBot.bat'; $Shortcut.WorkingDirectory = '%%INSTALL_DIR%%'; $Shortcut.Description = 'SmartWebBot Desktop App'; $Shortcut.Save^(^)"
echo.
echo echo Creating launcher...
echo ^(
echo echo @echo off
echo echo title SmartWebBot
echo echo cd /d "%%%%~dp0"
echo echo taskkill /F /IM python.exe /FI "WINDOWTITLE eq *backend*" ^^^>nul 2^^^>^^^&1
echo echo taskkill /F /IM node.exe ^^^>nul 2^^^>^^^&1
echo echo start /B "SmartWebBot Backend" python backend_server.py
echo echo timeout /t 5 /nobreak ^^^>nul
echo echo cd frontend
echo echo start "SmartWebBot Frontend" cmd /k "npm start"
echo echo echo SmartWebBot is starting...
echo echo pause
echo ^) ^> "%%INSTALL_DIR%%\SmartWebBot.bat"
echo.
echo echo.
echo echo ╔════════════════════════════════════════╗
echo echo ║  Installation Complete!               ║
echo echo ╚════════════════════════════════════════╝
echo echo.
echo echo SmartWebBot has been installed successfully!
echo echo.
echo echo Installation location: %%INSTALL_DIR%%
echo echo Desktop shortcut: SmartWebBot
echo echo.
echo echo To run SmartWebBot:
echo echo 1. Double-click the "SmartWebBot" shortcut on your desktop
echo echo 2. Wait for the app to start
echo echo 3. Your browser will open automatically
echo echo.
echo pause
) > "%PACKAGE_DIR%\INSTALL.bat"

echo [4/6] Creating README file...
(
echo # SmartWebBot Desktop App v2.0
echo ## Easy Installation Package
echo.
echo ### What is SmartWebBot?
echo.
echo SmartWebBot is an AI-powered web automation tool that helps you:
echo - Automate repetitive web tasks
echo - Extract data from websites
echo - Fill forms automatically
echo - Test web security
echo - Monitor web applications
echo.
echo ### Installation Requirements
echo.
echo Before installing SmartWebBot, you need:
echo.
echo 1. **Python 3.8 or higher**
echo    - Download from: https://www.python.org/downloads/
echo    - During installation, check "Add Python to PATH"
echo.
echo 2. **Node.js LTS version**
echo    - Download from: https://nodejs.org/
echo    - Install with default settings
echo.
echo ### Installation Steps
echo.
echo 1. Extract this ZIP file to any location
echo 2. Double-click `INSTALL.bat`
echo 3. Wait for the installation to complete
echo 4. Double-click the "SmartWebBot" shortcut on your desktop
echo.
echo ### First Time Use
echo.
echo When you first launch SmartWebBot:
echo - The backend server will start automatically
echo - The frontend will open in your browser
echo - Go to http://localhost:3000 to use the app
echo.
echo ### Features
echo.
echo - **Dashboard**: Overview of bot status and metrics
echo - **Task Builder**: Create automation tasks visually
echo - **Live Monitor**: Watch your bot work in real-time
echo - **AI Assistant**: Chat with AI for task guidance
echo - **Security Scanner**: Test websites for vulnerabilities
echo - **Results Viewer**: Export and analyze collected data
echo.
echo ### Troubleshooting
echo.
echo **App won't start:**
echo - Make sure Python and Node.js are installed
echo - Check that no other app is using ports 3000 or 8000
echo - Try running as Administrator
echo.
echo **Browser doesn't open:**
echo - Manually go to http://localhost:3000
echo - Check that the backend is running at http://localhost:8000
echo.
echo **Need help?**
echo - Check the logs in the terminal window
echo - Visit the API docs at http://localhost:8000/docs
echo.
echo ### System Requirements
echo.
echo - **OS**: Windows 10 or higher
echo - **RAM**: 4GB minimum ^(8GB recommended^)
echo - **Disk Space**: 2GB for installation
echo - **Internet**: Required for AI features
echo.
echo ### Uninstallation
echo.
echo To remove SmartWebBot:
echo 1. Delete the SmartWebBot folder from your Desktop
echo 2. Delete the SmartWebBot shortcut from your Desktop
echo.
echo ---
echo.
echo **Enjoy using SmartWebBot!** 🤖
) > "%PACKAGE_DIR%\README.txt"

echo [5/6] Creating quick start guide...
(
echo ╔════════════════════════════════════════╗
echo ║  SmartWebBot - Quick Start Guide     ║
echo ╚════════════════════════════════════════╝
echo.
echo STEP 1: Install Prerequisites
echo ==============================
echo.
echo Before installing SmartWebBot, install these:
echo.
echo 1. Python 3.8+
echo    → https://www.python.org/downloads/
echo    ⚠ Check "Add Python to PATH" during install!
echo.
echo 2. Node.js LTS
echo    → https://nodejs.org/
echo    ⚠ Use default installation settings
echo.
echo STEP 2: Install SmartWebBot
echo ============================
echo.
echo 1. Extract the ZIP file
echo 2. Double-click: INSTALL.bat
echo 3. Wait for installation to finish
echo.
echo STEP 3: Launch SmartWebBot
echo ===========================
echo.
echo → Double-click the "SmartWebBot" shortcut on your desktop
echo.
echo The app will:
echo - Start the backend server
echo - Start the frontend
echo - Open your browser automatically
echo.
echo STEP 4: Start Automating!
echo ==========================
echo.
echo Go to: http://localhost:3000
echo.
echo Try these features:
echo → Dashboard: See system status
echo → Task Builder: Create automation tasks
echo → AI Assistant: Get help from AI
echo → Live Monitor: Watch bot in action
echo.
echo ════════════════════════════════════════
echo.
echo Need Help?
echo - API Docs: http://localhost:8000/docs
echo - Check README.txt for details
echo.
echo ════════════════════════════════════════
) > "%PACKAGE_DIR%\QUICK_START.txt"

echo [6/6] Creating distribution package...
echo.
echo Compressing files into distributable ZIP...

powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%\*' -DestinationPath '%PACKAGE_NAME%.zip' -Force"

if exist "%PACKAGE_NAME%.zip" (
    echo.
    echo ╔════════════════════════════════════════╗
    echo ║  SUCCESS!                             ║
    echo ╚════════════════════════════════════════╝
    echo.
    echo Distributable package created: %PACKAGE_NAME%.zip
    echo Size: 
    for %%A in ("%PACKAGE_NAME%.zip") do echo %%~zA bytes
    echo.
    echo ════════════════════════════════════════
    echo HOW TO DISTRIBUTE:
    echo ════════════════════════════════════════
    echo.
    echo 1. Share the ZIP file: %PACKAGE_NAME%.zip
    echo 2. Tell users to extract it
    echo 3. Tell users to run INSTALL.bat
    echo.
    echo The installer will guide them through:
    echo - Checking Python and Node.js
    echo - Installing SmartWebBot
    echo - Creating desktop shortcut
    echo.
    echo ════════════════════════════════════════
    echo.
) else (
    echo.
    echo [ERROR] Failed to create ZIP package
    echo.
)

echo Cleaning up temporary files...
rmdir /s /q "%PACKAGE_DIR%"

echo.
echo Press any key to exit...
pause >nul
