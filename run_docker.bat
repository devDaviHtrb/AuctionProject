@echo off
REM ------------------------------------------
REM Uso:
REM   run_docker.bat              -> lift the container normally
REM   run_docker.bat -d           -> knocks down containers and packages.
REM ------------------------------------------

setlocal enabledelayedexpansion

set FLAG=%1

if "%FLAG%"=="-h" (
    echo Uso: %~nx0 [-d]
    echo   -d    Run "docker-compose down -v" before starting.
    exit /b 0
)
if "%FLAG%"=="--help" (
    echo Uso: %~nx0 [-d]
    echo   -d    Run "docker-compose down -v" before starting.
    exit /b 0
)

if "%FLAG%"=="-d" (
    echo Knocking down containers and packages...
    docker-compose down -v
    if errorlevel 1 (
        echo Error removing containers.
        exit /b 1
    )
    echo Containers successfully removed.
)

echo Uploading containers...
docker-compose up --build
if errorlevel 1 (
    echo Error building containers.
    exit /b 1
)

echo Containers running successfully.
endlocal
exit /b 0
