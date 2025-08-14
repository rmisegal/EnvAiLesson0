@echo off
title Ollama Troubleshooting

echo ================================================================
echo                  OLLAMA TROUBLESHOOTING
echo ================================================================
echo.

echo [STEP 1] Checking Ollama Installation...
echo ----------------------------------------------------------------

set "OLLAMA_PATH=D:\AI_Environment\Ollama"
set "OLLAMA_EXE=%OLLAMA_PATH%\ollama.exe"

if exist "%OLLAMA_EXE%" (
    echo [OK] Ollama executable found at: %OLLAMA_EXE%
) else (
    echo [ERROR] Ollama executable NOT found at: %OLLAMA_EXE%
    echo.
    echo Checking alternative locations...
    
    if exist "D:\AI_Environment\Ollama\" (
        echo [INFO] Ollama directory exists, checking contents:
        dir "D:\AI_Environment\Ollama\"
    ) else (
        echo [ERROR] Ollama directory does not exist
        echo This suggests Ollama was not installed properly.
        echo Please re-run the installer.
        pause
        exit /b 1
    )
    pause
    exit /b 1
)

echo.
echo [STEP 2] Checking PATH Configuration...
echo ----------------------------------------------------------------

echo Current PATH entries containing Ollama:
echo %PATH% | findstr /i ollama
if %errorlevel% neq 0 (
    echo [WARNING] Ollama not found in PATH
    echo Saving original PATH...
    set "ORIGINAL_PATH=%PATH%"
    echo [OK] Original PATH saved
    
    echo Adding Ollama to PATH for this session...
    set "PATH=%OLLAMA_PATH%;%PATH%"
    echo [OK] Ollama added to PATH
    echo.
    echo To restore original PATH later, use:
    echo   set "PATH=%ORIGINAL_PATH%"
) else (
    echo [OK] Ollama found in PATH
)

echo.
echo [STEP 3] Testing Ollama Executable...
echo ----------------------------------------------------------------

echo Testing Ollama with full path...
"%OLLAMA_EXE%" --help >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ollama executable works with full path
) else (
    echo [ERROR] Ollama executable failed to run
    echo This could be a permission or antivirus issue.
)

echo.
echo Testing Ollama command...
ollama --help >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ollama command works from PATH
) else (
    echo [WARNING] Ollama command not working from PATH
    echo Using full path for remaining tests...
)

echo.
echo [STEP 4] Checking Ollama Server Status...
echo ----------------------------------------------------------------

echo Checking if Ollama server is running...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe">NUL
if %errorlevel% equ 0 (
    echo [OK] Ollama server is running
) else (
    echo [INFO] Ollama server is not running
    echo Starting Ollama server...
    start /B "" "%OLLAMA_EXE%" serve
    timeout /t 5 /nobreak >nul
    
    tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe">NUL
    if %errorlevel% equ 0 (
        echo [OK] Ollama server started successfully
    ) else (
        echo [WARNING] Ollama server may not have started
    )
)

echo.
echo [STEP 5] Testing Ollama Commands...
echo ----------------------------------------------------------------

echo Testing ollama version...
if exist "%OLLAMA_EXE%" (
    "%OLLAMA_EXE%" --version 2>nul
    if %errorlevel% equ 0 (
        echo [OK] Ollama version command works
    ) else (
        echo [WARNING] Ollama version command failed
    )
) else (
    echo [ERROR] Cannot test - executable not found
)

echo.
echo Testing ollama list...
if exist "%OLLAMA_EXE%" (
    "%OLLAMA_EXE%" list 2>nul
    if %errorlevel% equ 0 (
        echo [OK] Ollama list command works
    ) else (
        echo [INFO] Ollama list failed (server may not be ready)
    )
) else (
    echo [ERROR] Cannot test - executable not found
)

echo.
echo ================================================================
echo                      SOLUTIONS
echo ================================================================
echo.

if not exist "%OLLAMA_EXE%" (
    echo PROBLEM: Ollama not installed
    echo SOLUTION: Re-run the AI Environment installer
    echo   1. Run: install.bat --step 7
    echo   2. This will reinstall Ollama and models
    echo.
    goto :end
)

echo IMMEDIATE FIX - Add Ollama to PATH:
echo ----------------------------------------------------------------
echo Option 1 - Temporary fix (for current session):
echo   Save original: set "ORIGINAL_PATH=%%PATH%%"
echo   Add Ollama: set "PATH=D:\AI_Environment\Ollama;%%PATH%%"
echo   Test: ollama list
echo   Restore later: set "PATH=%%ORIGINAL_PATH%%"
echo.
echo Option 2 - Use full path:
echo   D:\AI_Environment\Ollama\ollama.exe list
echo   D:\AI_Environment\Ollama\ollama.exe run llama2
echo.
echo Option 3 - Fix activation script:
echo   Edit D:\AI_Environment\activate_ai_env.bat
echo   Ensure it saves original PATH first
echo.

echo PERMANENT FIX - Update activate_ai_env.bat:
echo ----------------------------------------------------------------
echo The activation script should include these lines:
echo   set "OLLAMA_PATH=D:\AI_Environment\Ollama"
echo   set "PATH=%%OLLAMA_PATH%%;%%PATH%%"
echo.
echo Check if these lines exist in your activate_ai_env.bat file.
echo.

:end
echo ================================================================
echo.
echo ENVIRONMENT SAFETY:
echo ----------------------------------------------------------------
echo If you modified PATH during this troubleshooting:
echo   Restore original: set "PATH=%ORIGINAL_PATH%"
echo.
echo For complete environment restoration:
echo   Run: restore_environment.bat
echo.
echo QUICK TEST COMMANDS:
echo   D:\AI_Environment\Ollama\ollama.exe --version
echo   D:\AI_Environment\Ollama\ollama.exe list  
echo   D:\AI_Environment\Ollama\ollama.exe serve
echo.
pause
