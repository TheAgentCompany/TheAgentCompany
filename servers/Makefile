SHELL = /bin/bash

HOSTNAME?=ogma.lti.cs.cmu.edu
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
	$(MAKE) rm-rocketchat-volume

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
	docker volume rm servers_mongodb_data

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
start-api-server: init
	docker run -d \
		--name api-server \
		--network host \
		--restart always \
		-v /var/run/docker.sock:/var/run/docker.sock \
		ghcr.io/theagentcompany/servers-api-server:latest

start-api-server-with-setup: init
	docker run -d \
		--name api-server \
		--network host \
		--restart always \
		-e SKIP_SETUP=True \
		-v /var/run/docker.sock:/var/run/docker.sock \
		ghcr.io/theagentcompany/servers-api-server:latest

stop-api-server:
	docker stop api-server

rm-api-server: stop-api-server
	docker rm api-server
