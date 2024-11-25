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
	docker compose up -d
	make start-plane
	make start-rocketchat
	make start-sotopia-redis

stop-all: init
	docker compose down
	$(MAKE) rm-rocketchat-volume

# GitLab
start-gitlab: init
	docker compose up gitlab -d

stop-gitlab:
	docker compose stop gitlab

# rebuild destroys the gitlab image and start from scratch
# useful when you have new data to bake into the image
# Note: this will take at least 10 hours to build since we have quite a few
# large repositories to bake into the image
rebuild-gitlab: init
	@echo "stopping existing gitlab instance..."
	docker compose stop gitlab
	@echo "remove gitlab container..."
	docker compose rm gitlab
	@if docker image inspect servers-gitlab >/dev/null 2>&1; then \
		echo "Image servers-gitlab exists. Removing..."; \
		docker image rm servers-gitlab; \
	else \
		echo "Image servers-gitlab does not exist. Skipping removal."; \
	fi
	@echo "rebuild gitlab from clean state..."
	@echo "Before building, please make sure you have modified docker-compose.yml according to the instructions in the comments."
	docker compose build --no-cache gitlab

# reset stops the gitlab container, destroys and starts again
# any changes to gitlab will disappear, and the container will start
# in a clean state (with pre-populated data)
reset-gitlab: init
	@echo "stopping existing gitlab instance..."
	docker compose stop gitlab
	@echo "remove gitlab container..."
	docker compose rm -f gitlab
	@echo "start gitlab from clean state..."
	docker compose up gitlab -d

# RocketChat
start-rocketchat: init
	docker compose up rocketchat -d
	python ./rocketchat/restore_data.py

stop-rocketchat:
	docker compose stop rocketchat
	docker compose stop mongodb

rm-rocketchat:
	docker compose rm -f rocketchat
	docker compose rm -f mongodb
	make rm-rocketchat-volume

rm-rocketchat-volume:
	docker volume rm servers_mongodb_data

reset-rocketchat:
	docker exec -i servers-mongodb-1 sh -c 'mongorestore --drop --archive' < ./rocketchat/db.dump

backup-rocketchat:
	docker exec servers-mongodb-1 sh -c 'mongodump --archive' > ./rocketchat/db.dump


# Sotopia Redis
start-sotopia-redis: init
	docker compose up -d redis-stack redis-stack-npc-data-population

stop-sotopia-redis:
	docker compose stop redis-stack redis-stack-npc-data-population

rm-sotopia-redis:
	docker compose rm -f redis-stack redis-stack-npc-data-population

attach-sotopia-redis:
	docker exec -it redis-stack /bin/bash

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
	cd plane && make rm-plane-volume

reset-plane:
	cd plane && make reset-plane

start-owncloud:
	docker compose up owncloud owncloud-collabora -d

stop-owncloud:
	docker compose stop owncloud owncloud-collabora

reset-owncloud: init
	@echo "stopping existing owncloud instance..."
	docker compose stop owncloud owncloud-collabora
	@echo "remove owncloud container..."
	docker compose rm -f owncloud owncloud-collabora
	@echo "start owncloud from clean state..."
	docker compose up owncloud owncloud-collabora -d

