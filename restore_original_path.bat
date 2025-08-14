@echo off
title Restore Original Windows PATH

echo ================================================================
echo                   Restore Original Windows PATH
echo                  Remove All D: Drive AI Paths
echo ================================================================
echo.

echo [*] Current PATH contains D: drive paths - cleaning...
echo.

:: Enable delayed expansion for variable handling
setlocal EnableDelayedExpansion

:: Get current PATH
set "CURRENT_PATH=%PATH%"

:: Rebuild clean PATH without any D:\AI_Environment entries
set "CLEAN_PATH="
for %%i in ("%CURRENT_PATH:;=" "%") do (
    set "ENTRY=%%~i"
    if not "!ENTRY!"=="" (
        :: Skip any D:\AI_Environment paths
        echo !ENTRY! | findstr /i /c:"D:\AI_Environment" >nul
        if errorlevel 1 (
            :: This entry doesn't contain D:\AI_Environment, so keep it
            if defined CLEAN_PATH (
                set "CLEAN_PATH=!CLEAN_PATH!;!ENTRY!"
            ) else (
                set "CLEAN_PATH=!ENTRY!"
            )
        ) else (
            echo [REMOVED] !ENTRY!
        )
    )
)

:: Set the cleaned PATH and end local scope
endlocal & set "PATH=%CLEAN_PATH%"

echo.
echo [OK] Original Windows PATH restored
echo [INFO] All D:\AI_Environment paths removed
echo.

:: Verify basic Windows commands work
echo [*] Testing basic Windows commands...
where cmd >nul 2>&1 && echo [OK] 'where' command working || echo [ERROR] 'where' command not working
dir >nul 2>&1 && echo [OK] 'dir' command working || echo [ERROR] 'dir' command not working
tasklist >nul 2>&1 && echo [OK] 'tasklist' command working || echo [ERROR] 'tasklist' command not working

echo.
echo [*] Deactivating any conda environments...
conda deactivate >nul 2>&1
set "CONDA_DEFAULT_ENV="
set "CONDA_PREFIX="

echo.
echo ================================================================
echo                    PATH RESTORATION COMPLETE
echo ================================================================
echo.
echo Original Windows PATH has been restored.
echo All D: drive AI Environment paths have been removed.
echo Basic Windows commands should now work properly.
echo.
echo To activate AI Environment with clean start:
echo   D:\AI_Environment\activate_ai_env.bat
echo.
pause

