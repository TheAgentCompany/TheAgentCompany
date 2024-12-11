################## check 'docker' and 'docker compose' installation ######### 
echo "Checking if docker is installed..."
if ! command -v docker >/dev/null 2>&1; then \
    echo "Error: docker is not installed"; \
    echo "Please install docker first"; \
    exit 1; \
fi

echo "Checking if docker compose is installed..."
if ! docker compose version >/dev/null 2>&1; then \
    echo "Error: docker compose is not installed or docker daemon is not running"; \
    echo "Please install docker compose"; \
    exit 1; \
fi

echo "✓ Docker is installed"
docker version
echo "\n✓ Docker Compose is installed"
docker compose version

################## pull docker image ################## 
echo "Starting Pull Image..."
docker pull ghcr.io/theagentcompany/servers-api-server:1.0.0
docker pull ghcr.io/theagentcompany/servers-rocketchat-npc-data-population:1.0.0
docker pull ghcr.io/theagentcompany/servers-owncloud:1.0.0
docker pull ghcr.io/theagentcompany/servers-gitlab:1.0.0
docker pull ghcr.io/theagentcompany/servers-plane-admin:1.0.0
docker pull ghcr.io/theagentcompany/servers-plane-frontend:1.0.0
docker pull ghcr.io/theagentcompany/servers-plane-backend:1.0.0
docker pull ghcr.io/theagentcompany/servers-plane-space:1.0.0
docker pull ghcr.io/theagentcompany/servers-plane-proxy:1.0.0
docker pull minio/minio:RELEASE.2024-11-07T00-52-20Z
docker pull collabora/code:24.04.9.2.1
docker pull busybox:1.37.0
docker pull docker:27.3.1
docker pull valkey/valkey:7.2.5-alpine
docker pull redis/redis-stack-server:7.4.0-v0
docker pull postgres:15.7-alpine
docker pull bitnami/mongodb:5.0
docker pull registry.rocket.chat/rocketchat/rocket.chat:5.3.0

################## setup service ################## 
echo "Starting Setup service"
docker stop api-server
docker rm api-server
docker run -d \
    --name api-server \
    --network host \
    --restart always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    ghcr.io/theagentcompany/servers-api-server:1.0.0

# wait for service launching
echo "Waiting for service launching..."
sleep 120

echo "Checking if api-server is running on port 2999..."
until curl -s -o /dev/null localhost:2999; do \
    echo "Waiting for api-server to start on port 2999..."; \
    sleep 15; \
done
echo "api-server is running on port 2999!"

echo "Starting health checks..."
for service in rocketchat owncloud gitlab plane; do \
    until curl -s -o /dev/null -w "%{http_code}" localhost:2999/api/healthcheck/$service | grep -q "200"; do \
        echo "Waiting for $service to be ready..."; \
        sleep 10; \
    done; \
    echo "$service is ready!"; \
done
echo "All services are up and running!"
echo "Setup Finished!"