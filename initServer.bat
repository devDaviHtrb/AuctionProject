@echo off
REM Caminho relativo para o Python do venv
set PYTHON_PATH=C:\Users\Micro\OneDrive\Documentos\IFSP\2025\Tec\LabProgm\AuctionProject\.venv\Scripts\python.exe

REM Caminho do seu app Flask
set FLASK_APP=C:\Users\Micro\OneDrive\Documentos\IFSP\2025\Tec\LabProgm\AuctionProject\app.py

REM Iniciar Flask em nova janela
start cmd /k "%PYTHON_PATH% %FLASK_APP%"

REM Aguarda 2 segundos para o Flask iniciar
timeout /t 2 /nobreak >nul

REM Rodar ngrok usando caminho absoluto ou relativo
"C:\ngrok\ngrok.exe" http 5000

pause
