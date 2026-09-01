@echo off
title Valve Tests
cd /d "c:\Users\crd\OneDrive\Documents\GitHub\valve-tests-2"

where poetry >nul 2>&1
if errorlevel 1 (
    echo Poetry is not installed or not on the PATH.
    echo Please contact the person who set this up.
    echo.
    pause
    exit /b 1
)

echo Starting program. Close this window or press Ctrl+C to stop.
echo.
poetry run python main.py

echo.
echo Program stopped.
pause
