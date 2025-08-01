@echo off
title Automation Control Center
echo 🚀 Starting Automation Control Center...

:: Activate the venv using a path relative to the script's location
CALL "%~dp0.venv\Scripts\activate"

echo.
echo Running the main application...
python "%~dp0start.py"

echo.
echo Automation has finished. Press any key to exit.
pause