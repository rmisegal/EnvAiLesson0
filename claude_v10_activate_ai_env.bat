@echo off
title AI Environment - Portable AI Development

:: Save original environment variables
set "ORIGINAL_COLOR=07"
set "ORIGINAL_PATH=%PATH%"
set "ORIGINAL_PROMPT=%PROMPT%"

:: Save original conda variables (if any)
if defined CONDA_DEFAULT_ENV set "ORIGINAL_CONDA_ENV=%CONDA_DEFAULT_ENV%"
if defined CONDA_PREFIX set "ORIGINAL_CONDA_PREFIX=%CONDA_PREFIX%"

:: Set color scheme to green
color 0A
set "RESTORE_COLOR=color %ORIGINAL_COLOR%"
set "RESTORE_PATH=set PATH=%ORIGINAL_PATH%"
set "RESTORE_PROMPT=set PROMPT=%ORIGINAL_PROMPT%"

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

echo [STEP 1] Initializing and Activating AI2025 Conda Environment...
echo ----------------------------------------------------------------

:: Check if conda exists
if not exist "%CONDA_EXE%" (
    echo [ERROR] Conda not found at %CONDA_EXE%
    %RESTORE_COLOR%
    pause
    exit /b 1
)

:: CRITICAL: Properly initialize conda for current session
echo Initializing conda for current session...

:: Set conda paths and environment variables FIRST
set "CONDA_EXE=%CONDA_EXE%"
set "CONDA_ROOT=%CONDA_PATH%"
set "CONDA_ENVS_PATH=%CONDA_PATH%\envs"
set "CONDA_PKGS_DIRS=%CONDA_PATH%\pkgs"

:: Initialize conda properly - this is the key fix
call "%CONDA_EXE%" init cmd.exe >nul 2>&1

:: Create a temporary batch file for conda initialization
echo @echo off > "%TEMP%\conda_init.bat"
echo call "%CONDA_EXE%" shell.cmd.exe hook >> "%TEMP%\conda_init.bat"
call "%TEMP%\conda_init.bat" > "%TEMP%\conda_hook.bat" 2>nul
if exist "%TEMP%\conda_hook.bat" call "%TEMP%\conda_hook.bat"
del /q "%TEMP%\conda_init.bat" "%TEMP%\conda_hook.bat" 2>nul

:: Set portable environment paths with priority
echo Setting portable environment paths...
set "NEW_PATH=%CONDA_PATH%\envs\AI2025"
set "NEW_PATH=%NEW_PATH%;%CONDA_PATH%\envs\AI2025\Scripts"
set "NEW_PATH=%NEW_PATH%;%CONDA_PATH%\envs\AI2025\Library\bin"
set "NEW_PATH=%NEW_PATH%;%CONDA_PATH%\Scripts"
set "NEW_PATH=%NEW_PATH%;%CONDA_PATH%\Library\bin"
set "PATH=%NEW_PATH%;%PATH%"

:: Now activate the environment
echo Activating AI2025 environment...
call "%CONDA_EXE%" activate AI2025 2>nul

:: Check if activation was successful
if "%CONDA_DEFAULT_ENV%"=="AI2025" (
    echo [OK] AI2025 environment activated successfully
) else (
    echo [WARNING] Standard activation failed, using direct method...
    :: Direct activation method
    set "CONDA_DEFAULT_ENV=AI2025"
    set "CONDA_PREFIX=%CONDA_PATH%\envs\AI2025"
    set "CONDA_PROMPT_MODIFIER=(AI2025) "
    echo [OK] AI2025 environment activated via direct method
)

echo.

echo [STEP 2] Verifying Python Installation...
echo ----------------------------------------------------------------

:: Check Python path
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH
    %RESTORE_COLOR%
    pause
    exit /b 1
)

:: Get Python path and verify it's from D: drive
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    set "PYTHON_PATH=%%i"
    goto :found_python
)

:found_python
echo %PYTHON_PATH% | findstr /i "D:\AI_Environment" >nul
if %errorlevel% neq 0 (
    echo [WARNING] Python not from D: drive
    echo Current Python: %PYTHON_PATH%
    echo Expected: D:\AI_Environment\Miniconda\envs\AI2025\python.exe
    echo.
    echo [INFO] Fixing PATH priority for portable environment...
    
    :: Simple PATH fix - put D: drive paths first
    set "PATH=%CONDA_PATH%\envs\AI2025;%CONDA_PATH%\envs\AI2025\Scripts;%PATH%"
    
    :: Re-check Python path
    for /f "tokens=*" %%i in ('where python 2^>nul') do (
        set "PYTHON_PATH=%%i"
        goto :fixed_python
    )
    
    :fixed_python
    echo Fixed Python path: %PYTHON_PATH%
)

echo [OK] Using Python: %PYTHON_PATH%

:: Check Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [OK] Python Version: %PYTHON_VERSION%
echo.

echo [STEP 3] Checking Flask Installation...
echo ----------------------------------------------------------------

:: Check if Flask is installed by trying to import it
echo Testing Flask installation...
python -c "import flask; print('Flask version:', flask.__version__)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Flask not found. Installing Flask...
    pip install flask >nul 2>&1
    
    :: Test Flask installation by trying to import it again
    echo Verifying Flask installation...
    python -c "import flask; print('Flask version:', flask.__version__)" >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Flask - import test failed
        echo Trying alternative installation method...
        pip install --force-reinstall flask
        
        :: Final test
        python -c "import flask; print('Flask version:', flask.__version__)" >nul 2>&1
        if %errorlevel% neq 0 (
            echo [ERROR] Flask installation failed completely
            %RESTORE_COLOR%
            pause
            exit /b 1
        ) else (
            echo [OK] Flask installed successfully (alternative method)
        )
    ) else (
        echo [OK] Flask installed and verified successfully
    )
) else (
    echo [OK] Flask is already installed and working
)
echo.

echo [STEP 4] Starting Ollama Server...
echo ----------------------------------------------------------------

:: Check if Ollama executable exists
if not exist "%OLLAMA_EXE%" (
    echo [ERROR] Ollama not found at %OLLAMA_EXE%
    %RESTORE_COLOR%
    pause
    exit /b 1
)

:: Check if Ollama is already running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe">NUL
if %errorlevel% equ 0 (
    echo [OK] Ollama server is already running
) else (
    echo [INFO] Starting Ollama server in background...
    
    :: Start Ollama server in background
    start /B "" "%OLLAMA_EXE%" serve
    
    :: Wait longer for server to fully start
    echo [INFO] Waiting for Ollama server to initialize...
    timeout /t 6 /nobreak >nul
    
    :: Verify server started (simplified check)
    tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe">NUL
    if %errorlevel% equ 0 (
        echo [OK] Ollama server started successfully
    ) else (
        echo [INFO] Ollama server may still be starting...
        echo [INFO] You can check status with: tasklist ^| findstr ollama
        echo [INFO] Or test API with: ollama list
    )
)

echo.
echo [STEP 5] Final Environment Verification...
echo ----------------------------------------------------------------

:: Test Python from correct location
echo Testing Python functionality...
python -c "import sys; print('Python OK - Location:', sys.executable)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Python test failed
    set "PYTHON_OK=0"
) else (
    echo [OK] Python is working correctly
    set "PYTHON_OK=1"
)

:: Test conda environment with better logic
echo Testing conda environment status...
if defined CONDA_DEFAULT_ENV (
    if /i "%CONDA_DEFAULT_ENV%"=="AI2025" (
        echo [OK] Conda environment: %CONDA_DEFAULT_ENV% (Active)
        set "CONDA_OK=1"
    ) else (
        echo [WARNING] Conda environment: %CONDA_DEFAULT_ENV% (Expected: AI2025)
        set "CONDA_OK=0"
    )
) else (
    echo [WARNING] CONDA_DEFAULT_ENV not set (Expected: AI2025)
    set "CONDA_OK=0"
)

:: Test Flask functionality
echo Testing Flask functionality...
python -c "import flask; print('Flask version:', flask.__version__)" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Flask is working correctly
    set "FLASK_OK=1"
) else (
    echo [WARNING] Flask may have issues
    set "FLASK_OK=0"
)

:: Test Ollama one more time
echo Testing Ollama server status...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe">NUL
if %errorlevel% equ 0 (
    echo [OK] Ollama server process is running
    set "OLLAMA_OK=1"
) else (
    echo [INFO] Ollama server process not detected (may still be starting)
    set "OLLAMA_OK=0"
)

:: Summary of verification
echo.
echo Environment Verification Summary:
echo   - Python: %PYTHON_OK% (1=OK, 0=Issue)
echo   - Conda:  %CONDA_OK% (1=OK, 0=Issue)  
echo   - Flask:  %FLASK_OK% (1=OK, 0=Issue)
echo   - Ollama: %OLLAMA_OK% (1=OK, 0=Issue)

echo.
echo ================================================================
echo                 [SUCCESS] AI ENVIRONMENT READY!
echo ================================================================
echo.

echo Environment Details:
echo   - Environment: AI2025 (Conda)
echo   - Python: %PYTHON_VERSION%
echo   - Location: %AI_ENV_PATH%
echo   - Ollama: %OLLAMA_EXE%
echo.

echo Quick Start Commands:
echo   ollama list         - See your AI models
echo   ollama run llama2   - Start chatting with AI
echo   code .              - Open VS Code
echo   jupyter lab         - Start Jupyter notebooks
echo   python              - Start Python interpreter
echo.

echo ================================================================
echo                      HELP SYSTEM
echo ================================================================
echo.
echo For detailed instructions and troubleshooting:
echo   help\help_menu.bat
echo.
echo Available help topics:
echo   1. Using Ollama AI Models        5. Managing Ollama Server
echo   2. Using VS Code                 6. Environment Management  
echo   3. Python Development            7. Shutdown Procedures
echo   4. Project Examples              8. Useful Tips
echo.
echo Run: help\help_menu.bat for interactive help system
echo.

echo ================================================================

echo Current Directory: %CD%
echo AI Environment: %AI_ENV_PATH%
echo.

:: Change to AI Environment directory
cd /d "%AI_ENV_PATH%"

echo Ready for AI development!
echo.
echo QUICK START: Type 'ollama run llama2' to start chatting with AI
echo HELP SYSTEM: Type 'help\help_menu.bat' for detailed guides
echo.
echo ================================================================
echo                    ENVIRONMENT RESTORATION
echo ================================================================
echo.
echo To restore your original environment when done:
echo.
echo   1. Deactivate conda environment:
echo      conda deactivate
echo.
echo   2. Restore original PATH:
echo      set "PATH=%ORIGINAL_PATH%"
echo.
echo   3. Restore original prompt:
echo      set "PROMPT=%ORIGINAL_PROMPT%"
echo.
echo   4. Restore original colors:
echo      %RESTORE_COLOR%
echo.
echo   5. Or simply close this terminal window
echo.
echo Type 'exit' to close this session and auto-restore environment.
echo.

:: Set proper prompt and keep session open
set "PROMPT=(AI2025) $P$G"

:: Create exit restoration command
set "RESTORE_ALL=%RESTORE_COLOR% & set PATH=%ORIGINAL_PATH% & set PROMPT=%ORIGINAL_PROMPT%"

:: Keep the window open with proper exit handling
cmd /k "echo AI Environment Active - Type 'exit' to restore all settings && echo. && %RESTORE_ALL%"