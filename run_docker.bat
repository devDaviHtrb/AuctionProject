@echo off
REM 
SETLOCAL ENABLEEXTENSIONS

docker-compose build

docker-compose up -d

docker ps

pause
