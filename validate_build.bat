@echo off
REM Validation script for Heimdall Windows build configuration
REM This script checks if all prerequisites are met before building

echo ====================================
echo Heimdall Build Validation
echo ====================================
echo.

REM Initialize validation result
set VALIDATION_PASSED=1

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python is not installed or not in PATH
    set VALIDATION_PASSED=0
) else (
    for /f "tokens=*" %%i in ('python --version') do echo [PASS] %%i
)

echo.
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] pip is not available
    set VALIDATION_PASSED=0
) else (
    for /f "tokens=*" %%i in ('python -m pip --version') do echo [PASS] %%i
)

echo.
echo Checking Python version (3.8+ required)...
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Python 3.8 or higher is required
    set VALIDATION_PASSED=0
) else (
    echo [PASS] Python version is compatible
)

echo.
echo Checking for required build files...

if not exist "setup.py" (
    echo [FAIL] setup.py not found
    set VALIDATION_PASSED=0
) else (
    echo [PASS] setup.py found
)

if not exist "pyproject.toml" (
    echo [FAIL] pyproject.toml not found
    set VALIDATION_PASSED=0
) else (
    echo [PASS] pyproject.toml found
)

if not exist "heimdall.spec" (
    echo [FAIL] heimdall.spec not found
    set VALIDATION_PASSED=0
) else (
    echo [PASS] heimdall.spec found
)

if not exist "src\heimdall\main.py" (
    echo [FAIL] src\heimdall\main.py not found
    set VALIDATION_PASSED=0
) else (
    echo [PASS] src\heimdall\main.py found
)

echo.
echo Checking if PyInstaller is installed...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [WARN] PyInstaller is not installed
    echo        This is required for building. Run: pip install pyinstaller
) else (
    echo [PASS] PyInstaller is installed
)

echo.
echo ====================================
if %VALIDATION_PASSED%==1 (
    echo Result: All required checks passed!
    echo You can proceed with building by running:
    echo   build_windows.bat
) else (
    echo Result: Some checks failed
    echo Please fix the issues above before building
)
echo ====================================
echo.

pause
