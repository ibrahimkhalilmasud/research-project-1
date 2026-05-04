@echo off
title MR MIKE — Research Dashboard Fix & Launch
color 0E

echo.
echo  =====================================================
echo   RESEARCH DASHBOARD — FIX ^& LAUNCH  v2.0
echo  =====================================================
echo.

:: ── Use Miniconda's tools directly ───────────────────────────────────────
set CONDA_PIP=C:\Users\USER\Miniconda3\Scripts\pip.exe
set CONDA_STREAMLIT=C:\Users\USER\Miniconda3\Scripts\streamlit.exe

:: Verify pip exists
if not exist "%CONDA_PIP%" (
    echo  [ERROR] Miniconda pip not found at:
    echo  %CONDA_PIP%
    echo.
    echo  Please run "INSTALL FIRST (run once).bat" first.
    echo.
    pause
    exit /b 1
)

:: ── Step 1: Upgrade starlette to version compatible with current Streamlit ─
echo  [1/4] Upgrading starlette to compatible version...
"%CONDA_PIP%" install "starlette>=0.46.0" --quiet 2>nul
echo        Done.

:: ── Step 2: Ensure Streamlit is up to date ───────────────────────────────
echo  [2/4] Ensuring Streamlit is current...
"%CONDA_PIP%" install "streamlit>=1.35.0" --quiet 2>nul
echo        Done.

:: ── Step 3: Ensure all dashboard dependencies are present ────────────────
echo  [3/4] Checking dashboard dependencies...
"%CONDA_PIP%" install watchdog openpyxl pandas --quiet 2>nul
echo        Done.

:: ── Step 4: Launch ───────────────────────────────────────────────────────
echo  [4/4] Launching dashboard...
echo.
echo  =====================================================
echo   URL  :  http://localhost:8501
echo   STOP :  Close this window or press Ctrl+C
echo  =====================================================
echo.

cd /d "%~dp0"
"%CONDA_STREAMLIT%" run research_dashboard.py ^
    --server.headless false ^
    --browser.gatherUsageStats false ^
    --server.port 8501 ^
    --server.fileWatcherType poll

pause
