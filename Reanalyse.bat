@echo off
title PB Calorimeter - Re-analysis
cd /d "%~dp0"

where poetry >nul 2>&1
if errorlevel 1 (
    echo Poetry is not installed or not on the PATH.
    echo Please contact the person who set this up.
    echo.
    pause
    exit /b 1
)

echo Re-analysing an existing results file.
echo Drag a CSV onto this file to choose it, or pick one from the dialog.
echo.
poetry run python reanalyse.py %*

echo.
echo Program stopped.
pause
