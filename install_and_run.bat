@echo off
cd /d %~dp0
echo === IQBOT: Preparando entorno ===
if not exist venv (
  echo Creando entorno virtual...
  py -3 -m venv venv || python -m venv venv
)
echo Activando entorno...
call venv\Scripts\activate.bat
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
echo Iniciando la app...
py app.py || python app.py
pause
