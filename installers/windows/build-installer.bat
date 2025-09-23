@echo off
echo ========================================
echo SmartWebBot Windows Installer Builder
echo ========================================

echo.
echo [1/6] Checking prerequisites...

:: Check if NSIS is installed
where makensis >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: NSIS not found!
    echo Please install NSIS from: https://nsis.sourceforge.io/
    echo Add NSIS to your PATH environment variable.
    pause
    exit /b 1
)
echo ✅ NSIS found

:: Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ and add to PATH.
    pause
    exit /b 1
)
echo ✅ Python found

echo.
echo [2/6] Creating portable Python bundle...

:: Create Python bundle directory
if exist "python-bundle" rmdir /s /q "python-bundle"
mkdir "python-bundle"

:: Download portable Python (if not exists)
if not exist "python-3.11.9-embed-amd64.zip" (
    echo Downloading Python 3.11.9 portable...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip' -OutFile 'python-3.11.9-embed-amd64.zip'"
)

:: Extract Python
powershell -Command "Expand-Archive -Path 'python-3.11.9-embed-amd64.zip' -DestinationPath 'python-bundle' -Force"

:: Download get-pip.py
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'python-bundle/get-pip.py'"

:: Install pip in portable Python
python-bundle\python.exe python-bundle\get-pip.py --target python-bundle\Lib\site-packages

:: Enable site-packages in portable Python
echo import site >> python-bundle\python311._pth
echo site.main() >> python-bundle\python311._pth

:: Install SmartWebBot dependencies
python-bundle\python.exe -m pip install -r "..\..\requirements.txt" --target python-bundle\Lib\site-packages --no-warn-script-location

echo ✅ Python bundle created

echo.
echo [3/6] Creating portable Node.js bundle...

:: Create Node.js bundle directory
if exist "nodejs-bundle" rmdir /s /q "nodejs-bundle"
mkdir "nodejs-bundle"

:: Download Node.js portable (if not exists)
if not exist "node-v18.17.0-win-x64.zip" (
    echo Downloading Node.js 18.17.0...
    powershell -Command "Invoke-WebRequest -Uri 'https://nodejs.org/dist/v18.17.0/node-v18.17.0-win-x64.zip' -OutFile 'node-v18.17.0-win-x64.zip'"
)

:: Extract Node.js
powershell -Command "Expand-Archive -Path 'node-v18.17.0-win-x64.zip' -DestinationPath 'temp-node' -Force"
xcopy "temp-node\node-v18.17.0-win-x64\*" "nodejs-bundle\" /E /I /H /Y
rmdir /s /q "temp-node"

:: Install frontend dependencies
cd nodejs-bundle
npm install --prefix . "..\..\..\..\frontend"
cd ..

echo ✅ Node.js bundle created

echo.
echo [4/6] Creating launcher executable...

:: Create a simple launcher script
echo @echo off > SmartWebBot-Launcher.bat
echo cd /d "%%~dp0" >> SmartWebBot-Launcher.bat
echo set PATH=%%~dp0python-bundle;%%~dp0nodejs-bundle;%%PATH%% >> SmartWebBot-Launcher.bat
echo start "" "%%~dp0python-bundle\python.exe" "%%~dp0start_desktop_app.py" >> SmartWebBot-Launcher.bat

:: Convert batch to exe (requires Bat To Exe Converter or similar)
:: For now, we'll use the batch file directly
copy SmartWebBot-Launcher.bat SmartWebBot.exe

echo ✅ Launcher created

echo.
echo [5/6] Creating assets...

:: Create assets directory
if not exist "assets" mkdir "assets"

:: Create a simple icon (you should replace this with actual icons)
echo Creating placeholder icon...
echo. > assets\icon.ico
echo. > assets\welcome.bmp

echo ✅ Assets prepared

echo.
echo [6/6] Building installer...

:: Build the installer with NSIS
makensis SmartWebBot-Setup.nsi

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ SUCCESS! Installer created successfully!
    echo ========================================
    echo.
    echo 📦 Installer: SmartWebBot-Setup.exe
    echo 📏 Size: 
    dir SmartWebBot-Setup.exe | findstr SmartWebBot-Setup.exe
    echo.
    echo 🎉 Ready for distribution!
    echo Users can now just double-click to install SmartWebBot
    echo.
) else (
    echo.
    echo ========================================
    echo ❌ ERROR: Failed to build installer!
    echo ========================================
    echo Please check the output above for errors.
    echo.
)

echo Press any key to exit...
pause >nul
