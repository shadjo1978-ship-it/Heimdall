@echo off
REM Windows build script for Heimdall
REM This script builds a standalone Windows executable

echo ====================================
echo Heimdall Windows Build Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    exit /b 1
)

echo Step 1: Installing build dependencies...
python -m pip install --upgrade pip
python -m pip install pyinstaller wheel setuptools

echo.
echo Step 2: Installing Heimdall dependencies...
python -m pip install -e .

echo.
echo Step 3: Building Windows executable...
pyinstaller heimdall.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo Error: Build failed!
    exit /b 1
)

echo.
echo ====================================
echo Build completed successfully!
echo ====================================
echo.
echo Executable location: dist\Heimdall.exe
echo.
echo To run Heimdall:
echo   cd dist
echo   Heimdall.exe
echo.

pause
