# Python Installation Script
Write-Host "Starting Python installation..." -ForegroundColor Green

# Python 3.12 latest version download URL
$pythonUrl = "https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe"
$installerPath = "$env:TEMP\python-installer.exe"

Write-Host "Downloading Python installer..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "Download completed!" -ForegroundColor Green
    
    Write-Host "Starting Python installation..." -ForegroundColor Yellow
    Write-Host "Please check 'Add Python to PATH' option during installation!" -ForegroundColor Cyan
    
    # Run Python installer with PATH addition
    Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
    
    Write-Host "Python installation completed!" -ForegroundColor Green
    Write-Host "Please restart the terminal and run:" -ForegroundColor Yellow
    Write-Host "  python --version" -ForegroundColor Cyan
    Write-Host "  pip install Flask" -ForegroundColor Cyan
    Write-Host "  python app.py" -ForegroundColor Cyan
    
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
} catch {
    Write-Host "Error occurred: $_" -ForegroundColor Red
    Write-Host "Please install Python manually:" -ForegroundColor Yellow
    Write-Host "1. Download Python from https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "2. Check 'Add Python to PATH' during installation" -ForegroundColor Cyan
    Write-Host "3. Restart terminal after installation" -ForegroundColor Cyan
}
