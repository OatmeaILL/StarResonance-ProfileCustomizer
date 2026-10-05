@echo off
cd /d "%~dp0"

echo ==========================================
echo  StarResonance-ProfileCustomizer
echo ==========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    echo         Install Python 3.8+ and enable "Add Python to PATH".
    pause
    exit /b 1
)

python -c "import PyQt5, PIL, UnityPy, psutil" >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Missing dependencies. Install them with:
    echo         python -m pip install -r requirements.txt
    echo         If the download is slow, use a mirror:
    echo         python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    pause
    exit /b 1
)

python main.py

echo.
pause