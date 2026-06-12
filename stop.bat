@echo off
setlocal

REM Atlas Maroc Capital Markets - Static Website Stop Script (Windows)

echo [INFO] Stopping Python HTTP server...

REM Kill all Python HTTP server processes
for /f "tokens=2" %%a in ('tasklist /fi "imagename eq python.exe" ^| findstr "python.exe"') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo [SUCCESS] Server stopped

endlocal
