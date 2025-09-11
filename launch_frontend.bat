@echo off
echo Launching SmartWebBot Desktop Frontend...
set PATH=C:\Program Files\nodejs;%PATH%
cd frontend
npm run electron
