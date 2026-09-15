@echo off
cd /d C:\Users\maruk\Desktop\union_health_v2

start "LINE HOME - Django" cmd /k "venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000"

timeout /t 3 /nobreak >nul

start "LINE HOME - ngrok" cmd /k "ngrok http 8000"

exit