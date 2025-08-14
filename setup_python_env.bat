@echo off
setlocal EnableDelayedExpansion

:: Setup Python Environment for AI Environment Manager v3.0.22
:: This script prepares the environment before running Python code

set "SCRIPT_VERSION=3.0.22"
set "SCRIPT_DATE=2025-08-13"
set "VERBOSE_MODE=0"

:: Check for --verbose parameter
if "%1"=="--verbose" set "VERBOSE_MODE=1"
if "%2"=="--verbose" set "VERBOSE_MODE=1"

title Setting up Python Environment v%SCRIPT_VERSION%

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] setup_python_env.bat v%SCRIPT_VERSION% ^(%SCRIPT_DATE%^) starting
)

echo ================================================================
echo                  Python Environment Setup
echo                   Version %SCRIPT_VERSION% (%SCRIPT_DATE%)
echo                   Preparing for AI Manager
echo ================================================================
echo.

:: Define paths
set "AI_ENV_PATH=D:\AI_Environment"
set "CONDA_PATH=%AI_ENV_PATH%\Miniconda"
set "CONDA_ENV_PATH=%CONDA_PATH%\envs\AI2025"
set "PYTHON_EXE=%CONDA_ENV_PATH%\python.exe"

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] AI_ENV_PATH=%AI_ENV_PATH%
    echo [VERBOSE] CONDA_PATH=%CONDA_PATH%
    echo [VERBOSE] CONDA_ENV_PATH=%CONDA_ENV_PATH%
    echo [VERBOSE] PYTHON_EXE=%PYTHON_EXE%
)

echo [*] Step 1: Checking AI Environment structure
echo ----------------------------------------------------------------

:: Check if AI Environment exists
if not exist "%AI_ENV_PATH%" (
    echo [ERROR] AI Environment not found at %AI_ENV_PATH%
    echo Please ensure the AI Environment is installed on D: drive
    
    exit /b 1
)
echo [OK] AI Environment directory found

:: Check if Miniconda exists
if not exist "%CONDA_PATH%" (
    echo [ERROR] Miniconda not found at %CONDA_PATH%
    echo Please ensure Miniconda is installed in the AI Environment
    
    exit /b 1
)
echo [OK] Miniconda installation found

:: Check if AI2025 environment exists
if not exist "%CONDA_ENV_PATH%" (
    echo [ERROR] AI2025 conda environment not found at %CONDA_ENV_PATH%
    echo Please ensure the AI2025 environment is created
    
    exit /b 1
)
echo [OK] AI2025 conda environment found

:: Check if Python executable exists
if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python executable not found at %PYTHON_EXE%
    echo Please ensure Python is installed in the AI2025 environment
    
    exit /b 1
)
echo [OK] Python executable found

echo.
echo [*] Step 2: Setting up Python environment paths
echo ----------------------------------------------------------------

:: Set essential Windows paths first
set "ESSENTIAL_PATHS=C:\Windows\System32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0"

:: Set conda and Python paths (using Scripts instead of bin for Windows)
set "CONDA_PATHS=%CONDA_ENV_PATH%;%CONDA_ENV_PATH%\Scripts;%CONDA_ENV_PATH%\Library\bin;%CONDA_PATH%\Scripts;%CONDA_PATH%\Library\bin;%CONDA_PATH%\condabin"

:: Combine paths with D: drive taking priority
set "PATH=%CONDA_PATHS%;%ESSENTIAL_PATHS%;%PATH%"

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] CONDA_PATHS=%CONDA_PATHS%
    echo [VERBOSE] Updated PATH length: %PATH:~0,100%...
)

echo [OK] Python environment paths configured

echo.
echo [*] Step 3: Activating conda environment
echo ----------------------------------------------------------------

:: Initialize conda for current session
if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Initializing conda for current session
)
call "%CONDA_PATH%\Scripts\conda.exe" init cmd.exe --no-user >nul 2>&1

:: Activate AI2025 environment
if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Activating AI2025 environment
)
call "%CONDA_PATH%\Scripts\activate.bat" "%CONDA_ENV_PATH%" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Standard activation failed, using manual setup
    set "CONDA_DEFAULT_ENV=AI2025"
    set "CONDA_PREFIX=%CONDA_ENV_PATH%"
) else (
    echo [OK] AI2025 environment activated
)

echo.
echo [*] Step 4: Verifying Python setup
echo ----------------------------------------------------------------

:: Test Python executable
if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Testing Python executable: "%PYTHON_EXE%"
)
"%PYTHON_EXE%" --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python executable test failed
    
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%v in ('"%PYTHON_EXE%" --version 2^>^&1') do set "PYTHON_VERSION=%%v"
echo [OK] Python %PYTHON_VERSION% ready

:: Test conda command
if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Testing conda command
)
"%CONDA_PATH%\Scripts\conda.exe" --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Conda command not available
) else (
    for /f "tokens=2" %%v in ('"%CONDA_PATH%\Scripts\conda.exe" --version 2^>^&1') do set "CONDA_VERSION=%%v"
    echo [OK] Conda %CONDA_VERSION% ready
)

echo.
echo [*] Step 5: Checking required Python packages
echo ----------------------------------------------------------------

:: Check for required packages
if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Checking psutil package
)
"%PYTHON_EXE%" -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing psutil package
    "%PYTHON_EXE%" -m pip install psutil >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Failed to install psutil
    ) else (
        echo [OK] psutil package installed
    )
) else (
    echo [OK] psutil package available
)

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Checking colorama package
)
"%PYTHON_EXE%" -c "import colorama" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing colorama package
    "%PYTHON_EXE%" -m pip install colorama >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Failed to install colorama
    ) else (
        echo [OK] colorama package installed
    )
) else (
    echo [OK] colorama package available
)

echo.
echo ================================================================
echo                 PYTHON ENVIRONMENT READY
echo ================================================================
echo.
echo Environment: AI2025 (Conda)
echo Python: %PYTHON_VERSION%
echo Location: %AI_ENV_PATH%
echo.
echo [*] Python environment is now configured and ready
echo [*] You can now run Python scripts with full AI Environment support
echo.

if "%VERBOSE_MODE%"=="1" (
    echo [VERBOSE] Exporting environment variables
    echo [VERBOSE] AI_PYTHON_EXE=%PYTHON_EXE%
    echo [VERBOSE] AI_ENV_READY=1
)

:: Export environment variables for calling script
endlocal & (
    set "PATH=%PATH%"
    set "CONDA_DEFAULT_ENV=%CONDA_DEFAULT_ENV%"
    set "CONDA_PREFIX=%CONDA_PREFIX%"
    set "AI_PYTHON_EXE=%PYTHON_EXE%"
    set "AI_ENV_READY=1"
)

echo Ready to launch AI Environment Manager
echo.

