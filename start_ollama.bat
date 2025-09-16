@echo off
echo Starting Ollama server for SmartWebBot...
echo.

REM Start Ollama server in the background
start /B "Ollama Server" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama.exe" serve

REM Wait a moment for the server to start
timeout /t 3 /nobreak >nul

echo Ollama server started successfully!
echo You can now run your SmartWebBot application.
echo.
echo To stop Ollama, close this window or run: taskkill /f /im ollama.exe
echo.
pause
