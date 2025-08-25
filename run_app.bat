@echo off
cd /d %~dp0
if exist venv (
  call venv\Scripts\activate.bat
)
py app.py || python app.py
pause
