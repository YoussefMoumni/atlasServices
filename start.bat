@echo off
setlocal enabledelayedexpansion

REM Atlas Maroc Capital Markets - Static Website Start Script (Windows)

set "PROJECT_ROOT=%~dp0"
set "WEBSITE_DIR=%PROJECT_ROOT%website"
set "PID_FILE=%PROJECT_ROOT%.pids"

echo [INFO] Starting Atlas Maroc Capital Markets static website...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.
    echo Visit: https://www.python.org/downloads/
    exit /b 1
)

REM Find available port
set PORT=8000
:find_port
netstat -an | findstr ":%PORT%" >nul 2>&1
if not errorlevel 1 (
    set /a PORT+=1
    goto find_port
)

echo [INFO] Found available port: %PORT%

REM Start Python HTTP server
cd /d "%WEBSITE_DIR%"
start /B python -m http.server %PORT% >nul 2>&1

REM Wait for server to start
timeout /t 2 /nobreak >nul

echo.
echo ================================================
echo Atlas Maroc Capital Markets
echo ================================================
echo.
echo   Website URL:  http://localhost:%PORT%
echo.
echo Available Pages:
echo   * Overview:          http://localhost:%PORT%/
echo   * Advisory:          http://localhost:%PORT%/advisory.html
echo   * Brokerage:         http://localhost:%PORT%/brokerage.html
echo   * Asset Management:  http://localhost:%PORT%/asset-management.html
echo   * Research:          http://localhost:%PORT%/research.html
echo   * Capital Raising:   http://localhost:%PORT%/capital-raising.html
echo   * Trading:           http://localhost:%PORT%/trading.html
echo.
echo ================================================
echo.
echo Commands:
echo   * Stop server:  stop.bat
echo.

REM Open browser
start http://localhost:%PORT%

echo Press Ctrl+C to stop the server...
pause >nul
