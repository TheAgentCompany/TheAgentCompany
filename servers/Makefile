SHELL = /bin/bash

NEXTCLOUD_HOME?=/home/yufansong/data/nextcloud
HOSTNAME?=ogma.lti.cs.cmu.edu
FILE_SERVER_PORT?=8081
GITLAB_PORT?=8929
NEXTCLOUD_BACKUP_VOLUME_NAME?=nextcloud_aio_backupdir
NEXTCLOUD_BACKUP_VOLUME_PATH?=/home/yufansong/data/nextcloud
NEXTCLOUD_IMAGE_TAG?=20240808_083748
NEXTCLOUD_PORT?=8090
PLANE_DOCKER_FILE_PATH=./plane/plane-app/docker-compose.yaml
PLANE_DOCKER_ENV_PATH=./plane/plane-app/plane.env

.PHONY: init start-all stop-all start-file-server stop-file-server start-gitlab stop-gitlab rebuild-gitlab reset-gitlab \
		create-nextcloud-backup-volume rm-nextcloud-backup-volume rm-nextcloud-volume stop-nextcloud-side-container \
		rm-nextcloud-side-container get-nextcloud-config enter-nextcloud-container \
		start-rocketchat stop-rocketchat rm-rocketchat rm-rocketchat-volume reset-rocketchat backup-rocketchat

init:
	$(eval export NEXTCLOUD_HOME)
	$(eval export HOSTNAME)
	$(eval export GITLAB_PORT)
	$(eval export NEXTCLOUD_IMAGE_TAG)
	$(eval export NEXTCLOUD_PORT)
	@echo "Initialization done."

start-all: init
	docker compose up -d

stop-all: init rm-nextcloud-volume
	docker compose down
	$(MAKE) rm-nextcloud-volume
	$(MAKE) rm-rocketchat-volume

# Nextcloud
create-nextcloud-backup-volume:
	docker volume create \
		--driver local \
		--name $(NEXTCLOUD_BACKUP_VOLUME_NAME) \
		-o device=$(NEXTCLOUD_BACKUP_VOLUME_PATH) \
		-o type="none" \
		-o o="bind"

rm-nextcloud-backup-volume:
	docker volume rm $(NEXTCLOUD_BACKUP_VOLUME_NAME)

rm-nextcloud-volume: rm-nextcloud-side-container
	docker volume ls -q --filter "name=nextcloud" | grep -v "nextcloud_aio_backupdir" | xargs -r docker volume rm

stop-nextcloud-side-container:
	docker ps -q --filter "name=nextcloud" | xargs -r docker stop

rm-nextcloud-side-container: stop-nextcloud-side-container
	docker ps -a -q --filter "name=nextcloud" | xargs -r docker rm

get-nextcloud-config:
	docker exec nextcloud-aio-mastercontainer cat /mnt/docker-aio-config/data/configuration.json

enter-nextcloud-container:
	docker exec -it nextcloud-aio-mastercontainer /bin/bash

# NOTE: when start nextcloud, please make sure NEXTCLOUD_BACKUP_VOLUME_PATH is empty
start-nextcloud: init create-nextcloud-backup-volume
	docker compose up nextcloud -d

stop-nextcloud: init stop-nextcloud-side-container
	docker compose stop nextcloud

rm-nextcloud: init rm-nextcloud-volume rm-nextcloud-side-container
	docker compose rm nextcloud
	docker network rm nextcloud-aio
	docker volume rm nextcloud_aio_backupdir
	docker volume rm nextcloud_aio_nextcloud_datadir
	make rm-nextcloud-backup-volume
	docker network rm servers_nextcloud-network

backup-nextcloud:
	./nextcloud/backup.sh

reset-nextcloud:
	./nextcloud/restore.sh
	docker exec nextcloud-aio-nextcloud chown -R 33:0 /mnt/ncdata/ 
	docker exec nextcloud-aio-nextcloud chmod -R 750 /mnt/ncdata/ 
	docker exec --user www-data -it nextcloud-aio-nextcloud php occ files:scan --all

# GitLab
start-gitlab: init
	docker compose up gitlab -d

stop-gitlab:
	docker compose stop gitlab

# rebuild destroys the gitlab image and start from scratch
# useful when you have new data to bake into the image
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
	@echo "start gitlab from clean state..."
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
	sh ./plane/download.sh

start-plane:
	sh ./plane/download.sh
	docker compose -f $(PLANE_DOCKER_FILE_PATH) --env-file $(PLANE_DOCKER_ENV_PATH)  up -d --quiet-pull

stop-plane:
	docker compose -f $(PLANE_DOCKER_FILE_PATH) --env-file $(PLANE_DOCKER_ENV_PATH) down

backup-plane:
	./plane/setup.sh backup

rm-plane-volume:
	docker volume rm plane-app_redisdata
	docker volume rm plane-app_uploads
	docker volume rm plane-app_logs_api
	docker volume rm plane-app_logs_beat-worker
	docker volume rm plane-app_logs_migrator
	docker volume rm plane-app_logs_worker
	docker volume rm plane-app_pgdata

reset-plane:
	make stop-plane
	./plane/restore.sh ./plane/
	make start-plane

