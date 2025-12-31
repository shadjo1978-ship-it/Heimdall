#!/usr/bin/env pwsh
# PowerShell build script for Heimdall (Windows)
# This script builds a standalone Windows executable

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Heimdall Windows Build Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Step 1: Installing build dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install pyinstaller wheel setuptools

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install build dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Installing Heimdall dependencies..." -ForegroundColor Yellow
python -m pip install -e .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install Heimdall dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Building Windows executable..." -ForegroundColor Yellow
pyinstaller heimdall.spec --clean --noconfirm

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable location: dist\Heimdall.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run Heimdall:" -ForegroundColor Yellow
Write-Host "  cd dist" -ForegroundColor White
Write-Host "  .\Heimdall.exe" -ForegroundColor White
Write-Host ""
