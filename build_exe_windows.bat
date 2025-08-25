@echo off
cd /d %~dp0
echo === IQBOT: Construyendo ejecutable (.exe) ===
if not exist venv (
  echo Creando entorno virtual...
  py -3 -m venv venv || python -m venv venv
)
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller iqbot.spec
echo.
echo Listo. Busca el ejecutable en: dist\app\app.exe
pause
