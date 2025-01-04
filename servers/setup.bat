@echo off
setlocal enabledelayedexpansion

REM Check Docker installation
echo Checking if docker is installed...
where docker >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: docker is not installed
    echo Please install docker first
    exit /b 1
)

echo Checking if docker compose is installed...
docker compose version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: docker compose is not installed or docker daemon is not running
    echo Please install docker compose
    exit /b 1
)

echo ✓ Docker is installed
docker version
echo:
echo ✓ Docker Compose is installed
docker compose version

REM Pull docker images
echo Starting Pull Image...
docker pull ghcr.io/theagentcompany/servers-api-server:latest
docker pull ghcr.io/theagentcompany/servers-rocketchat-npc-data-population:latest
docker pull ghcr.io/theagentcompany/servers-owncloud:latest
docker pull ghcr.io/theagentcompany/servers-gitlab:latest
docker pull ghcr.io/theagentcompany/servers-plane-admin:0.0.1
docker pull ghcr.io/theagentcompany/servers-plane-frontend:0.0.1
docker pull ghcr.io/theagentcompany/servers-plane-backend:0.0.1
docker pull ghcr.io/theagentcompany/servers-plane-space:0.0.1
docker pull ghcr.io/theagentcompany/servers-plane-proxy:0.0.1
docker pull minio/minio:RELEASE.2024-11-07T00-52-20Z
docker pull collabora/code:24.04.9.2.1
docker pull busybox:1.37.0
docker pull docker:27.3.1
docker pull valkey/valkey:7.2.5-alpine
docker pull redis/redis-stack-server:7.4.0-v0
docker pull postgres:15.7-alpine
docker pull bitnami/mongodb:5.0
docker pull registry.rocket.chat/rocketchat/rocket.chat:5.3.0

REM Setup service
echo Starting Setup service
docker stop api-server
docker rm api-server
docker run -d ^
    --name api-server ^
    --network host ^
    --restart always ^
    -v /var/run/docker.sock:/var/run/docker.sock ^
    ghcr.io/theagentcompany/servers-api-server:latest

REM Wait for service launching
echo Waiting for service launching...
timeout /t 120 /nobreak

echo Checking if api-server is running on port 2999...
:check_api
curl -s -o nul localhost:2999
if %ERRORLEVEL% neq 0 (
    echo Waiting for api-server to start on port 2999...
    timeout /t 15 /nobreak
    goto check_api
)
echo api-server is running on port 2999!

echo Starting health checks...
for %%s in (rocketchat owncloud gitlab plane) do (
    :check_service_%%s
    curl -s -o nul -w "%%{http_code}" localhost:2999/api/healthcheck/%%s | findstr "200" >nul
    if %ERRORLEVEL% neq 0 (
        echo Waiting for %%s to be ready...
        timeout /t 10 /nobreak
        goto check_service_%%s
    )
    echo %%s is ready!
)

echo All services are up and running!
echo Setup Finished!