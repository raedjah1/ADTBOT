@echo off
title SmartWebBot Desktop App Installer
echo SmartWebBot Desktop App Installer
echo ==================================
echo.

set "INSTALL_DIR=%USERPROFILE%\Desktop\SmartWebBot"

echo Installing SmartWebBot to your desktop...
echo Installation directory: %INSTALL_DIR%
echo.

echo Creating installation directory...
if exist "%INSTALL_DIR%" (
    echo Removing old version...
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"

echo Copying application files...
xcopy /E /I /H /Y "SmartWebBot_Desktop_App\*" "%INSTALL_DIR%\"
copy /Y "launch_app_simple.py" "%INSTALL_DIR%\"
copy /Y "backend_server.py" "%INSTALL_DIR%\"
copy /Y "config.yaml" "%INSTALL_DIR%\"
copy /Y "requirements.txt" "%INSTALL_DIR%\"

echo Copying configuration files...
if exist "config" (
    xcopy /E /I /H /Y "config" "%INSTALL_DIR%\config\"
)

if exist "data" (
    xcopy /E /I /H /Y "data" "%INSTALL_DIR%\data\"
)

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\SmartWebBot.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\SmartWebBot.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'SmartWebBot Desktop App - Click to Launch'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo SmartWebBot has been installed to: %INSTALL_DIR%
echo A desktop shortcut "SmartWebBot" has been created.
echo.
echo To run SmartWebBot:
echo 1. Double-click the "SmartWebBot" shortcut on your desktop
echo 2. Choose option 1 for the full desktop app
echo.
echo The app will start with a beautiful desktop interface!
echo.
echo Press any key to exit...
pause >nul
