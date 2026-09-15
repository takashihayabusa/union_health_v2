@echo off
cd /d C:\Users\maruk\Desktop\union_health_v2

start "Django - LINE HOME" cmd /k "C:\Users\maruk\Desktop\union_health_v2\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000"

timeout /t 5 /nobreak >nul

start "ngrok - LINE HOME" cmd /k "ngrok http 8000"

exit