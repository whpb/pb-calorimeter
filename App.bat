@echo off
title PB Calorimeter
cd /d "%~dp0"

where poetry >nul 2>&1
if errorlevel 1 (
    echo Poetry is not installed or not on the PATH.
    echo Please contact the person who set this up.
    echo.
    pause
    exit /b 1
)

poetry run python app.py
