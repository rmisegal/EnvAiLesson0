@echo off
title AI Environment - Portable AI Development

:: Save original color scheme
for /f "tokens=*" %%i in ('echo prompt $E^| cmd') do set "ESC=%%i"
for /f %%a in ('echo prompt $H^| cmd') do set "BS=%%a"

:: Get current color (this is a workaround since there's no direct way to get current color)
:: We'll assume default is 07 (white on black) and restore to that
set "ORIGINAL_COLOR=07"

:: Set color scheme to green
color 0A

:: Set up color restoration on exit
set "RESTORE_COLOR=color %ORIGINAL_COLOR%"

echo.
echo ================================================================
echo                   AI Environment Activation
echo                    Portable AI Development
echo ================================================================
echo.

:: Set environment paths
set "AI_ENV_PATH=D:\AI_Environment"
set "CONDA_PATH=%AI_ENV_PATH%\Miniconda"
set "CONDA_EXE=%CONDA_PATH%\Scripts\conda.exe"
set "CONDA_ACTIVATE=%CONDA_PATH%\Scripts\activate.bat"
set "OLLAMA_PATH=%AI_ENV_PATH%\Ollama"
set "OLLAMA_EXE=%OLLAMA_PATH%\ollama.exe"

:: Check if AI Environment exists
if not exist "%AI_ENV_PATH%" (
    echo [ERROR] AI Environment not found at %AI_ENV_PATH%
    echo Please run the installer first.
    %RESTORE_COLOR%
    pause
    exit /b 1
)

echo [*] Pre-Activation Cleanup and Detection...
echo ----------------------------------------------------------------

:: Check if AI2025 environment is already active
if "%CONDA_DEFAULT_ENV%"=="AI2025" (
    echo [INFO] AI2025 environment already active - deactivating first...
    conda deactivate >nul 2>&1
    set "CONDA_DEFAULT_ENV="
    set "CONDA_PREFIX="
) else if not "%CONDA_DEFAULT_ENV%"=="" (
    echo [INFO] Conda environment '%CONDA_DEFAULT_ENV%' active - deactivating...
    conda deactivate >nul 2>&1
    set "CONDA_DEFAULT_ENV="
    set "CONDA_PREFIX="
) else (
    echo [INFO] No conda environment currently active
)

:: Check if Ollama server is running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe">NUL
if %errorlevel% equ 0 (
    echo [INFO] Stopping existing Ollama server...
    taskkill /IM ollama.exe /F >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo [OK] Ollama server stopped
) else (
    echo [INFO] No Ollama server currently running
)

:: Check for Python processes from D: drive
echo [INFO] Checking for D: drive Python processes...
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV ^| findstr /i "D:\\AI_Environment"') do (
    echo [INFO] Found D: drive Python process - terminating...
    taskkill /PID %%i /F >nul 2>&1
)

:: Reset PATH to clean state (remove only Python/conda paths, preserve Windows system paths)
echo [INFO] Resetting PATH variables for clean start...
set "ORIGINAL_PATH=%PATH%"

:: Enable delayed expansion for variable handling in loops
setlocal EnableDelayedExpansion

:: Define essential Windows paths that must be preserved
set "ESSENTIAL_PATHS=C:\Windows\System32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0"

:: Start with essential Windows paths
set "CLEAN_PATH=%ESSENTIAL_PATHS%"

:: Add back non-Python system paths
for %%i in ("%ORIGINAL_PATH:;=" "%") do (
    set "CURRENT_PATH=%%~i"
    :: Skip empty paths
    if not "!CURRENT_PATH!"=="" (
        :: Skip Python/Anaconda/conda related paths
        echo !CURRENT_PATH! | findstr /i /c:"python" /c:"anaconda" /c:"conda" /c:"miniconda" >nul
        if errorlevel 1 (
            :: Skip if already in essential paths
            echo !ESSENTIAL_PATHS! | findstr /i /c:"!CURRENT_PATH!" >nul
            if errorlevel 1 (
                set "CLEAN_PATH=!CLEAN_PATH!;!CURRENT_PATH!"
            )
        )
    )
)

:: Set the cleaned PATH and end local scope
endlocal & set "PATH=%CLEAN_PATH%"

echo [OK] Environment cleanup completed
echo.

echo [*] Step 1: Initializing and Activating AI2025 Conda Environment...
echo ----------------------------------------------------------------

:: Check if conda exists
if not exist "%CONDA_EXE%" (
    echo [ERROR] Conda not found at %CONDA_EXE%
    %RESTORE_COLOR%
    pause
    exit /b 1
)

:: Initialize conda for this session
echo Initializing conda for current session...
call "%CONDA_EXE%" init cmd.exe --no-user >nul 2>&1

:: CRITICAL: Set conda paths FIRST in PATH to override system Python
echo Setting portable environment paths...
set "PATH=%CONDA_PATH%\envs\AI2025;%CONDA_PATH%\envs\AI2025\Scripts;%CONDA_PATH%\envs\AI2025\Library\bin;%CONDA_PATH%\Scripts;%CONDA_PATH%\Library\bin;%PATH%"
set "CONDA_EXE=%CONDA_EXE%"
set "CONDA_DEFAULT_ENV=AI2025"
set "CONDA_PREFIX=%CONDA_PATH%\envs\AI2025"

:: Activate AI2025 environment using the activate script
echo Activating AI2025 environment...
if exist "%CONDA_ACTIVATE%" (
    call "%CONDA_ACTIVATE%" "%CONDA_PATH%\envs\AI2025"
) else (
    call "%CONDA_EXE%" activate "%CONDA_PATH%\envs\AI2025"
)

if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate AI2025 environment
    echo Trying alternative activation method...
    
    :: Alternative: Ensure environment variables are set correctly
    set "CONDA_DEFAULT_ENV=AI2025"
    set "CONDA_PREFIX=%CONDA_PATH%\envs\AI2025"
    :: PATH already set above with correct priority
    
    echo [WARNING] Using manual environment activation
)

echo [OK] AI2025 environment activated successfully
echo.

echo [*] Step 2: Verifying Python Installation...
echo ----------------------------------------------------------------

:: Check Python path
for /f "tokens=*" %%i in ('where python 2^>nul') do set "PYTHON_PATH=%%i"

if "%PYTHON_PATH%"=="" (
    echo [ERROR] Python not found in PATH
    %RESTORE_COLOR%
    pause
    exit /b 1
)

:: Verify it's the correct Python (from D: drive)
echo %PYTHON_PATH% | findstr /i "D:\AI_Environment" >nul
if %errorlevel% neq 0 (
    echo [WARNING] Python not from D: drive
    echo Current Python: %PYTHON_PATH%
    echo Expected: D:\AI_Environment\Miniconda\envs\AI2025\python.exe
    echo.
    echo [*] Fixing PATH priority for portable environment...
    
    :: Remove system Python paths from PATH temporarily
    set "TEMP_PATH=%PATH%"
    set "PATH="
    
    :: Add D: drive paths FIRST
    set "PATH=%CONDA_PATH%\envs\AI2025;%CONDA_PATH%\envs\AI2025\Scripts;%CONDA_PATH%\envs\AI2025\Library\bin"
    set "PATH=%PATH%;%CONDA_PATH%\Scripts;%CONDA_PATH%\Library\bin"
    
    :: Add back system paths (but they'll be lower priority)
    for %%i in ("%TEMP_PATH:;=" "%") do (
        echo %%i | findstr /i /v "Python" | findstr /i /v "Anaconda" | findstr /i /v "conda" >nul
        if not errorlevel 1 set "PATH=%PATH%;%%~i"
    )
    
    :: Re-check Python path
    for /f "tokens=*" %%i in ('where python 2^>nul') do set "PYTHON_PATH=%%i"
    echo Fixed Python path: %PYTHON_PATH%
)

echo [OK] Using Python: %PYTHON_PATH%

:: Check Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [OK] Python Version: %PYTHON_VERSION%
echo.

echo [*] Step 3: Checking Flask Installation...
echo ----------------------------------------------------------------

:: Check if Flask is installed
python -c "import flask; print('Flask version:', flask.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING]  Flask not found. Installing Flask...
    pip install flask
    if %errorlevel% neq 0 (
        echo [ERROR] ERROR: Failed to install Flask
        %RESTORE_COLOR%
        pause
        exit /b 1
    )
    echo [OK] Flask installed successfully
) else (
    echo [OK] Flask is already installed
)
echo.

echo [*] Step 4: Starting Ollama Server...
echo ----------------------------------------------------------------

:: Check if Ollama executable exists
if not exist "%OLLAMA_EXE%" (
    echo [ERROR] ERROR: Ollama not found at %OLLAMA_EXE%
    %RESTORE_COLOR%
    pause
    exit /b 1
)

:: Check if Ollama is already running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if %errorlevel% equ 0 (
    echo [OK] Ollama server is already running
) else (
    echo [*] Starting Ollama server in background...
    
    :: Start Ollama server in background
    start /B "" "%OLLAMA_EXE%" serve
    
    :: Wait a moment for server to start
    timeout /t 3 /nobreak >nul
    
    :: Verify server started
    tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
    if %errorlevel% equ 0 (
        echo [OK] Ollama server started successfully in background
    ) else (
        echo [ERROR] WARNING: Ollama server may not have started properly
    )
)

echo.
echo [INFO] Ollama Server Management:
echo   • To bring to foreground: Not applicable (running as service)
echo   • To check status: tasklist ^| findstr ollama
echo   • To stop server: taskkill /IM ollama.exe /F
echo   • To restart: taskkill /IM ollama.exe /F ^&^& start /B "" "%OLLAMA_EXE%" serve
echo.

echo [*] Step 5: Verifying Running Processes...
echo ----------------------------------------------------------------

set "PROCESSES_OK=1"

:: Check Python process (current session)
echo Checking Python process...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if %errorlevel% equ 0 (
    echo [OK] Python processes: Running
) else (
    echo [WARNING]  Python processes: Not detected (normal for interactive session)
)

:: Check Ollama process
echo Checking Ollama server...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if %errorlevel% equ 0 (
    echo [OK] Ollama server: Running
    
    :: Get Ollama models
    echo [INFO] Available Ollama models:
    "%OLLAMA_EXE%" list 2>nul
    if %errorlevel% neq 0 (
        echo [WARNING]  No models found or server not ready. You may need to download models:
        echo   • %OLLAMA_EXE% pull llama2:7b
        echo   • %OLLAMA_EXE% pull codellama:7b
        echo   • %OLLAMA_EXE% pull mistral:7b
        echo   • %OLLAMA_EXE% pull phi:2.7b
    )
) else (
    echo [ERROR] Ollama server: Not running
    set "PROCESSES_OK=0"
)

:: Check Conda environment
echo Checking Conda environment...
if "%CONDA_DEFAULT_ENV%"=="AI2025" (
    echo [OK] Conda environment: AI2025 (Active)
) else (
    echo [WARNING]  Conda environment: %CONDA_DEFAULT_ENV% (Expected: AI2025)
)

echo.
echo ================================================================
if "%PROCESSES_OK%"=="1" (
    echo                 [OK] AI ENVIRONMENT READY!
) else (
    echo                 [WARNING]  AI ENVIRONMENT PARTIALLY READY
)
echo ================================================================
echo.

echo [*] Environment Details:
echo   • Environment: AI2025 (Conda)
echo   • Python: %PYTHON_VERSION%
echo   • Location: %AI_ENV_PATH%
echo   • Ollama: %OLLAMA_EXE%
echo.

echo [*] Available Commands:
echo   • conda list          - Show installed packages
echo   • pip list            - Show pip packages
echo   • python              - Start Python interpreter
echo   • jupyter lab         - Start Jupyter Lab
echo   • code .              - Open VS Code
echo   • ollama list         - Show available models
echo   • ollama run MODEL    - Chat with AI model
echo.

echo [*] Management Commands:
echo   • tasklist ^| findstr ollama     - Check Ollama status
echo   • taskkill /IM ollama.exe /F     - Stop Ollama server
echo   • conda deactivate               - Deactivate AI2025 environment
echo   • validate.bat                   - Run environment validation
echo   • exit                           - Close session and restore colors
echo.

echo [*] To Completely Deactivate Environment:
echo   1. conda deactivate              - Deactivate conda environment
echo   2. taskkill /IM ollama.exe /F    - Stop Ollama server
echo   3. color 07                      - Restore terminal colors
echo   4. exit                          - Close session
echo.

echo [INFO] Current Directory: %CD%
echo [INFO] AI Environment: %AI_ENV_PATH%
echo.

:: Change to AI Environment directory
cd /d "%AI_ENV_PATH%"

echo Ready for AI development! [*]
echo.

:: Set up exit handler to restore color
echo Type 'exit' to close this session and restore terminal colors.
echo Or use the deactivation commands above for manual cleanup.
echo.

:: Keep the window open and ready for commands with color restoration on exit
cmd /k "echo AI Environment Active - Use 'conda deactivate' and 'exit' to close && set PROMPT=(AI2025) $P$G"

:: Restore color when exiting
%RESTORE_COLOR%

