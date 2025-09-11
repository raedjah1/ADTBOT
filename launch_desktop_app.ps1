# SmartWebBot Desktop App Launcher (PowerShell)
Write-Host "🤖 SmartWebBot Desktop App Launcher" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Add Node.js to PATH
$env:PATH += ";C:\Program Files\nodejs"

# Start backend in background
Write-Host "🚀 Starting Python backend..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "backend_server.py" -WindowStyle Hidden

# Wait for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "🖥️ Starting Electron frontend..." -ForegroundColor Green
Set-Location "frontend"
& "C:\Program Files\nodejs\npm.cmd" run electron

Write-Host "✅ SmartWebBot Desktop App launched successfully!" -ForegroundColor Green





