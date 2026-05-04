@echo off
title MR MIKE  Research Dashboard
color 0A

echo.
echo  =====================================================
echo   MR MIKE RESEARCH DASHBOARD  v2.0
echo  =====================================================
echo.

:: ── Locate Streamlit (tries Miniconda first, then PATH) ──────────────────
set STREAMLIT=
if exist "C:\Users\USER\Miniconda3\Scripts\streamlit.exe" (
    set STREAMLIT=C:\Users\USER\Miniconda3\Scripts\streamlit.exe
) else (
    where streamlit >nul 2>&1
    if %errorlevel% equ 0 (
        set STREAMLIT=streamlit
    ) else (
        echo  [ERROR] Streamlit not found.
        echo  Please run "INSTALL FIRST (run once).bat" first.
        echo.
        pause
        exit /b 1
    )
)

:: ── Verify dashboard script exists ───────────────────────────────────────
if not exist "%~dp0research_dashboard.py" (
    echo  [ERROR] research_dashboard.py not found.
    echo  Expected in: %~dp0
    echo.
    pause
    exit /b 1
)

echo  Launching...
echo.
echo  =====================================================
echo   URL  :  http://localhost:8501
echo   STOP :  Close this window or press Ctrl+C
echo  =====================================================
echo.

cd /d "%~dp0"
"%STREAMLIT%" run research_dashboard.py ^
    --server.headless false ^
    --browser.gatherUsageStats false ^
    --server.port 8501 ^
    --server.fileWatcherType poll

pause
