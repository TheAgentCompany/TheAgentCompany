SHELL = /bin/bash

GITLAB_HOME?=/home/boxuanli/jobbench_gitlab
NEXTCLOUD_HOME?=/home/yufansong/data
HOSTNAME?=ogma.lti.cs.cmu.edu
FILE_SERVER_PORT?=8081
GITLAB_PORT?=8929
NEXTCLOUD_BACKUP_VOLUME_NAME?=nextcloud_aio_backupdir
NEXTCLOUD_BACKUP_VOLUME_PATH?=/home/yufansong/data/backup
NEXTCLOUD_IMAGE_TAG?=20240808_083748
NEXTCLOUD_PORT?=8090

.PHONY: init start-all stop-all start-file-server stop-file-server start-gitlab stop-gitlab reset-gitlab \
		create-nextcloud-backup-volume rm-nextcloud-backup-volume rm-nextcloud-volume stop-nextcloud-side-container \
		rm-nextcloud-side-container get-nextcloud-config enter-nextcloud-container \
		start-rocketchat stop-rocketchat rm-rocketchat rm-rocketchat-volume restore-rocketchat backup-rocketchat

init:
	$(eval export GITLAB_HOME)
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

start-nextcloud: init create-nextcloud-backup-volume
	docker compose up nextcloud -d

stop-nextcloud: init stop-nextcloud-side-container
	docker compose stop nextcloud

rm-nextcloud: init rm-nextcloud-volume
	docker compose rm nextcloud

# GitLab
start-gitlab: init
	docker compose up gitlab -d

stop-gitlab:
	docker compose stop gitlab

reset-gitlab:
	echo "stopping existing gitlab instance..."
	docker compose stop gitlab
	echo "remove gitlab container..."
	docker compose rm gitlab
	echo "remove built gitlab image..."
	docker image rm servers-gitlab
	echo "remove existing gitlab data..."
	sudo rm -rf $(GITLAB_HOME)
	mkdir -p $(GITLAB_HOME)
	echo "start gitlab from clean state..."
	docker compose up gitlab -d

# RocketChat
start-rocketchat: init
	docker compose up rocketchat -d

stop-rocketchat:
	docker compose stop rocketchat

rm-rocketchat:
	docker compose rm rocketchat

rm-rocketchat-volume:
	docker volume rm rocketchat_mongodb_data

restore-rocketchat:
	docker exec -i rocketchat-mongodb-1 sh -c 'mongorestore --archive' < db.dump

backup-rocketchat:
	docker exec rocketchat-mongodb-1 sh -c 'mongodump --archive' > db.dump
