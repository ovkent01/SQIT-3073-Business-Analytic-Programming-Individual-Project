@echo off
echo Checking Python installation...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first from https://www.python.org/downloads/
    pause
    exit /b
)

echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Running the program...
python main.py

pause
