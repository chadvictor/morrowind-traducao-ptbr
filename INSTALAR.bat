@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 scripts\mwbr.py gui
  goto :done
)
where python >nul 2>nul
if not errorlevel 1 (
  python scripts\mwbr.py gui
  goto :done
)
echo Instale Python 3.10 ou superior de https://www.python.org/downloads/windows/
echo Marque Add python.exe to PATH e inclua Tcl/Tk. Depois execute novamente.
:done
echo.
pause
