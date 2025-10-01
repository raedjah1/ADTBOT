@echo off
title SmartWebBot Desktop App Installer
echo SmartWebBot Desktop App Installer
echo ==================================
echo.

set "INSTALL_DIR=%USERPROFILE%\Desktop\SmartWebBot"

echo This will install SmartWebBot to your desktop.
echo Installation directory: %INSTALL_DIR%
echo.

set /p confirm="Do you want to continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Installation cancelled.
    pause
    exit /b
)

echo.
echo Creating installation directory...
if exist "%INSTALL_DIR%" (
    echo Directory already exists. Removing old version...
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"

echo Copying application files...
xcopy /E /I /H /Y "SmartWebBot_Desktop_App\*" "%INSTALL_DIR%\"

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\SmartWebBot.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\SmartWebBot.bat'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'SmartWebBot Desktop App'; $Shortcut.Save()"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo SmartWebBot has been installed to: %INSTALL_DIR%
echo A desktop shortcut has been created.
echo.
echo To run SmartWebBot:
echo 1. Double-click the "SmartWebBot" shortcut on your desktop
echo 2. Or go to %INSTALL_DIR% and double-click "SmartWebBot.bat"
echo.
echo The app will start with a beautiful desktop interface!
echo.
pause
