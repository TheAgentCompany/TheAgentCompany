SHELL = /bin/bash

HOSTNAME?=localhost
FILE_SERVER_PORT?=8081
GITLAB_PORT?=8929
PLANE_DOCKER_FILE_PATH=./plane/plane-app/docker-compose.yaml
PLANE_DOCKER_ENV_PATH=./plane/plane-app/plane.env

.PHONY: init start-all stop-all start-file-server stop-file-server start-gitlab stop-gitlab rebuild-gitlab reset-gitlab \
		start-owncloud stop-owncloud reset-owncloud \
		start-rocketchat stop-rocketchat rm-rocketchat rm-rocketchat-volume reset-rocketchat backup-rocketchat

init:
	$(eval export HOSTNAME)
	$(eval export GITLAB_PORT)
	@echo "Initialization done."

start-all: init
	docker compose -p theagentcompany up -d
	make start-plane
	make start-rocketchat
	make start-sotopia-redis

stop-all: init
	docker compose -p theagentcompany down
	make rm-rocketchat-volume
	make stop-api-server

# GitLab
start-gitlab: init
	docker compose -p theagentcompany up gitlab -d

stop-gitlab:
	docker compose -p theagentcompany stop gitlab

# rebuild destroys the gitlab image and start from scratch
# useful when you have new data to bake into the image
# Note: this will take at least 10 hours to build since we have quite a few
# large repositories to bake into the image
rebuild-gitlab: init
	@echo "stopping existing gitlab instance..."
	docker compose -p theagentcompany stop gitlab
	@echo "remove gitlab container..."
	docker compose -p theagentcompany rm gitlab
	@if docker image inspect servers-gitlab >/dev/null 2>&1; then \
		echo "Image servers-gitlab exists. Removing..."; \
		docker image rm servers-gitlab; \
	else \
		echo "Image servers-gitlab does not exist. Skipping removal."; \
	fi
	@echo "rebuild gitlab from clean state..."
	@echo "Before building, please make sure you have modified docker-compose.yml according to the instructions in the comments."
	docker compose -p theagentcompany build --no-cache gitlab

# reset stops the gitlab container, destroys and starts again
# any changes to gitlab will disappear, and the container will start
# in a clean state (with pre-populated data)
reset-gitlab: init
	@echo "stopping existing gitlab instance..."
	docker compose -p theagentcompany stop gitlab
	@echo "remove gitlab container..."
	docker compose -p theagentcompany rm -f gitlab
	@echo "start gitlab from clean state..."
	docker compose -p theagentcompany up gitlab -d

# RocketChat
start-rocketchat: init
	docker compose -p theagentcompany up rocketchat -d
	python rocketchat/restore_data.py

stop-rocketchat:
	docker compose -p theagentcompany stop rocketchat
	docker compose -p theagentcompany stop mongodb

rm-rocketchat: stop-rocketchat
	docker compose -p theagentcompany rm -f rocketchat
	docker compose -p theagentcompany rm -f mongodb
	make rm-rocketchat-volume

rm-rocketchat-volume:
	docker volume rm -f servers_mongodb_data

reset-rocketchat:
	docker exec -i rocketchat-mongodb sh -c 'mongorestore --drop --archive' < ./rocketchat/db.dump

backup-rocketchat:
	docker exec rocketchat-mongodb sh -c 'mongodump --archive' > ./rocketchat/data_restore/db.dump

# Sotopia Redis
start-sotopia-redis: init
	docker compose -p theagentcompany up -d redis-stack redis-stack-npc-data-population

stop-sotopia-redis:
	docker compose -p theagentcompany stop redis-stack redis-stack-npc-data-population

rm-sotopia-redis:
	docker compose -p theagentcompany rm -f redis-stack redis-stack-npc-data-population

attach-sotopia-redis:
	docker exec -it redis-stack /bin/bash

reset-sotopia-redis: init
	@echo "stopping existing sotopia redis instance..."
	docker compose -p theagentcompany stop redis-stack redis-stack-npc-data-population
	@echo "remove sotopia redis container..."
	docker compose -p theagentcompany rm -f redis-stack redis-stack-npc-data-population
	@echo "start sotopia redis from clean state..."
	docker compose -p theagentcompany up redis-stack redis-stack-npc-data-population -d

# Plane
download-plane:
	cd plane && make download-setup

start-plane:
	cd plane && make start-plane

stop-plane:
	cd plane && make stop-plane

backup-plane:
	cd plane && make backup-plane

rm-plane-volume:
	-docker volume rm plane-app_redisdata
	-docker volume rm plane-app_uploads
	-docker volume rm plane-app_logs_api
	-docker volume rm plane-app_logs_beat-worker
	-docker volume rm plane-app_logs_migrator
	-docker volume rm plane-app_logs_worker
	-docker volume rm plane-app_pgdata
	-docker network rm plane-app_default
	cd plane && make rm-plane-volume

reset-plane:
	cd plane && make reset-plane

start-owncloud:
	docker compose -p theagentcompany up owncloud owncloud-collabora -d

stop-owncloud:
	docker compose -p theagentcompany stop owncloud owncloud-collabora

reset-owncloud: init
	@echo "stopping existing owncloud instance..."
	docker compose -p theagentcompany stop owncloud owncloud-collabora
	@echo "remove owncloud container..."
	docker compose -p theagentcompany rm -f owncloud owncloud-collabora
	@echo "start owncloud from clean state..."
	docker compose -p theagentcompany up owncloud owncloud-collabora -d

# api-server
start-api-server-with-setup: init
	docker stop api-server || true
	docker rm -f api-server
	docker run -d \
		--name api-server \
		--network host \
		--restart always \
		-v /var/run/docker.sock:/var/run/docker.sock \
		ghcr.io/theagentcompany/servers-api-server:1.0.0

start-api-server: init
	docker stop api-server || true
	docker rm -f api-server
	docker run -d \
		--name api-server \
		--network host \
		--restart always \
		-e SKIP_SETUP=True \
		-v /var/run/docker.sock:/var/run/docker.sock \
		ghcr.io/theagentcompany/servers-api-server:1.0.0

stop-api-server:
	docker stop api-server || true

rm-api-server: stop-api-server
	docker rm -f api-server

get-ip:
	curl ifconfig.me

pull-image:
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

check:
	@echo "Checking if docker is installed..."
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Error: docker is not installed"; \
		echo "Please install docker first"; \
		exit 1; \
	fi
	
	@echo "Checking if docker compose is installed..."
	@if ! docker compose version >/dev/null 2>&1; then \
		echo "Error: docker compose is not installed or docker daemon is not running"; \
		echo "Please install docker compose"; \
		exit 1; \
	fi
	
	@echo "✓ Docker is installed"
	docker version
	@echo "\n✓ Docker Compose is installed"
	docker compose version

health-check:
	@echo "Checking if api-server is running on port 2999..."
	@until curl -s -o /dev/null localhost:2999; do \
		echo "Waiting for api-server to start on port 2999..."; \
		sleep 15; \
	done
	@echo "api-server is running on port 2999!"

	@echo "Starting health checks..."
	@for service in rocketchat owncloud gitlab plane; do \
		until curl -s -o /dev/null -w "%{http_code}" localhost:2999/api/healthcheck/$$service | grep -q "200"; do \
			echo "Waiting for $$service to be ready..."; \
			sleep 10; \
		done; \
		echo "$$service is ready!"; \
	done
	@echo "All services are up and running!"

setup:
	@echo "Starting check docker installation"
	make check
	@echo "Starting Pull Image..."
	make pull-image
	@echo "Starting Setup service"
	make start-api-server-with-setup
	sleep 120
	@echo "Starting health check"
	make health-check
