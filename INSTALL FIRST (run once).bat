@echo off
title MR MIKE — Research Dashboard First Setup
color 0B

echo.
echo  =====================================================
echo   MR MIKE RESEARCH DASHBOARD — FIRST SETUP  v2.0
echo  =====================================================
echo.
echo  This installs all required Python packages.
echo  Only needs to be done ONCE.
echo.

:: ── Detect Python: prefer Miniconda, fall back to system Python ──────────
set PYTHON=
set PIP=

if exist "C:\Users\USER\Miniconda3\python.exe" (
    set PYTHON=C:\Users\USER\Miniconda3\python.exe
    set PIP=C:\Users\USER\Miniconda3\Scripts\pip.exe
    echo  [OK] Miniconda Python detected.
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON=python
        set PIP=pip
        echo  [OK] System Python detected.
    ) else (
        echo  [ERROR] Python not found.
        echo.
        echo  Please install Miniconda from:
        echo  https://docs.conda.io/en/latest/miniconda.html
        echo.
        pause
        exit /b 1
    )
)

echo.
echo  Installing packages — this may take a minute...
echo.

:: ── Core: Streamlit ──────────────────────────────────────────────────────
echo  [1/4] Installing Streamlit...
"%PIP%" install "streamlit>=1.35.0" --quiet
echo        Done.

:: ── Fix: Upgrade starlette (required by current Streamlit) ───────────────
echo  [2/4] Upgrading starlette for compatibility...
"%PIP%" install "starlette>=0.46.0" --quiet
echo        Done.

:: ── Dashboard deps ───────────────────────────────────────────────────────
echo  [3/4] Installing dashboard dependencies...
"%PIP%" install watchdog openpyxl pandas --quiet
echo        Done.

:: ── File watcher support ─────────────────────────────────────────────────
echo  [4/4] Installing file watcher support...
"%PIP%" install "watchdog>=3.0" --quiet
echo        Done.

echo.
echo  =====================================================
echo   SETUP COMPLETE
echo   Now double-click: "LAUNCH DASHBOARD.bat"
echo   Or run:          "FIX ^& LAUNCH DASHBOARD.bat"
echo   (if you ever see errors on startup)
echo  =====================================================
echo.
pause
