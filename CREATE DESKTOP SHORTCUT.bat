@echo off
title MR MIKE — Create Desktop Shortcut
color 0D

echo.
echo  =====================================================
echo   MR MIKE — CREATE DESKTOP SHORTCUT  v2.0
echo  =====================================================
echo.

set SCRIPT_DIR=%~dp0
set SHORTCUT=%USERPROFILE%\Desktop\Mr Mike Research Dashboard.lnk
set TARGET=%SCRIPT_DIR%LAUNCH DASHBOARD.bat

:: Verify target bat exists
if not exist "%TARGET%" (
    echo  [ERROR] LAUNCH DASHBOARD.bat not found in:
    echo  %SCRIPT_DIR%
    echo.
    pause
    exit /b 1
)

:: Create the shortcut via PowerShell
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $s = $ws.CreateShortcut('%SHORTCUT%'); ^
   $s.TargetPath = '%TARGET%'; ^
   $s.WorkingDirectory = '%SCRIPT_DIR%'; ^
   $s.IconLocation = 'shell32.dll,22'; ^
   $s.WindowStyle = 1; ^
   $s.Description = 'Mr Mike Research Dashboard — Click to launch'; ^
   $s.Save()"

if %errorlevel% equ 0 (
    echo  [OK] Desktop shortcut created:
    echo       "Mr Mike Research Dashboard"
    echo.
    echo  Double-click it anytime to open your dashboard.
) else (
    echo  [ERROR] Shortcut creation failed. Try running as Administrator.
)

echo.
pause
