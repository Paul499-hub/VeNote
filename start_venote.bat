@echo off
cd /d "%~dp0"

docker compose up -d
if errorlevel 1 exit /b 1

echo Waiting for Venote...
for /l %%i in (1,1,120) do (
    curl.exe --silent --fail --max-time 2 --output NUL http://127.0.0.1:48721/
    if not errorlevel 1 goto ready
    timeout /t 2 /nobreak >nul
)

echo Venote did not become ready. Check docker compose logs backend.
pause
exit /b 1

:ready
start "" "http://127.0.0.1:48721/ui/home"