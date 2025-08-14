@echo off
setlocal EnableDelayedExpansion

:: AI Environment Python Launcher v3.0.22
:: First sets up the Python environment, then launches the Python system

set "SCRIPT_VERSION=3.0.22"
set "SCRIPT_DATE=2025-08-13"
set "VERBOSE_MODE=0"

:: Check for --verbose parameter
if "%1"=="--verbose" set "VERBOSE_MODE=1"
if "%2"=="--verbose" set "VERBOSE_MODE=1"

title AI Environment Manager v%SCRIPT_VERSION%

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] run_ai_env.bat v%SCRIPT_VERSION% ^(%SCRIPT_DATE%^) starting
)

echo ================================================================
echo                AI Environment Python Launcher
echo                      Version %SCRIPT_VERSION% (%SCRIPT_DATE%)
echo ================================================================
echo.

:: Navigate to AI Environment directory
cd /d "D:\AI_Environment"

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Current directory: %CD%
    echo [VERBOSE] Checking for setup_python_env.bat
)

:: Check if setup script exists
if not exist "setup_python_env.bat" (
    echo [ERROR] setup_python_env.bat not found in D:\AI_Environment
    echo [ERROR] Please ensure all files are extracted correctly
    echo [INFO] Expected files:
    echo   - setup_python_env.bat
    echo   - activate_ai_env.py
    echo   - src\ai_*.py
    
    exit /b 1
)

:: Step 1: Setup Python environment
echo [INFO] Setting up Python environment
if "%VERBOSE_MODE%"=="1" (
    call setup_python_env.bat --verbose
) else (
    call setup_python_env.bat
)
if errorlevel 1 (
    echo [ERROR] Failed to setup Python environment
    echo [ERROR] Please check the error messages above
    
    exit /b 1
)

:: Step 2: Check if Python environment is ready
if not "%AI_ENV_READY%"=="1" (
    echo [ERROR] Python environment setup incomplete
    echo [ERROR] AI_ENV_READY flag not set
    if "%VERBOSE_MODE%"=="1" (
        echo [VERBOSE] Environment variables:
        echo [VERBOSE] AI_ENV_READY=%AI_ENV_READY%
        echo [VERBOSE] AI_PYTHON_EXE=%AI_PYTHON_EXE%
    )
    
    exit /b 1
)

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Python environment ready
    echo [VERBOSE] AI_PYTHON_EXE=%AI_PYTHON_EXE%
)

:: Step 3: Check if activation script exists
if not exist "src\activate_ai_env.py" (
    echo [ERROR] src\activate_ai_env.py not found
    echo Please ensure all Python files are in D:\AI_Environment\src
    if "%VERBOSE_MODE%"=="1" (
        echo [VERBOSE] Current directory contents:
        dir /b
        echo [VERBOSE] src directory contents:
        dir /b src\
    )
    
    exit /b 1
)

:: Step 4: Verify Python executable exists
if not exist "%AI_PYTHON_EXE%" (
    echo [ERROR] Python executable not found at: %AI_PYTHON_EXE%
    echo [ERROR] Please check your AI Environment installation
    
    exit /b 1
)

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Testing Python executable
    "%AI_PYTHON_EXE%" --version
    if errorlevel 1 (
        echo [VERBOSE] Python test failed
    ) else (
        echo [VERBOSE] Python test successful
    )
)

:: Step 5: Launch the Python activation system using the configured Python
echo [INFO] Starting AI Environment Manager
echo.

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Launching: "%AI_PYTHON_EXE%" src\activate_ai_env.py --verbose
    "%AI_PYTHON_EXE%" src\activate_ai_env.py --verbose
) else (
    "%AI_PYTHON_EXE%" src\activate_ai_env.py
)

:: Step 6: Cleanup and exit
echo.
echo [INFO] AI Environment Manager closed
if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] run_ai_env.bat v%SCRIPT_VERSION% completed
)


