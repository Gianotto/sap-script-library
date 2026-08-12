# SAP Script Manager - PowerShell Launcher
# Execute: .\run.ps1

$pythonPath = "C:\Users\vg72934\AppData\Local\Programs\Python\Python311\python.exe"
$appDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$appFile = Join-Path $appDir "app\sap_gui_manager.py"

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  SAP Script Manager                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verify Python
if (!(Test-Path $pythonPath)) {
    Write-Host "❌ Error: Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Python expected at:" -ForegroundColor Yellow
    Write-Host "  $pythonPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Solution:" -ForegroundColor Yellow
    Write-Host "  1. Install Python 3.11 from https://www.python.org" -ForegroundColor Yellow
    Write-Host "  2. Select 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host "  3. Restart this script" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Verify application
if (!(Test-Path $appFile)) {
    Write-Host "❌ Error: sap_gui_manager.py not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Looking in: $appFile" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Python detected: " -ForegroundColor Green -NoNewline
& $pythonPath --version

Write-Host "✅ Application: $appFile" -ForegroundColor Green
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Cyan
Write-Host ""

# Add app to PYTHONPATH
$env:PYTHONPATH = "$appDir\app;$env:PYTHONPATH"

# Run application
& $pythonPath $appFile

Write-Host ""
Write-Host "Application finished" -ForegroundColor Gray
