@echo off
chcp 65001 >nul
echo ========================================
echo Fin-Agent Web 可视化系统
echo ========================================
echo.
cd /d %~dp0
python run.py
pause
