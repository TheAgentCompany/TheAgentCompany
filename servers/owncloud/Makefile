IMAGE_NAME=owncloud
IMAGE_TAG=test

run:
	docker compose up -d
start:
	docker compose up -d
stop:
	docker compose down
rm:
	-docker network rm owncloud_owncloud_network
restart:
	-make stop
	-make rm
	-make start
	-docker exec -it ${IMAGE_NAME} bash

backup:
	rm -rf owncloud_data && docker cp owncloud:/var/www/html/data/theagentcompany ./owncloud_data
	rm -rf owncloud_apps && docker cp owncloud:/var/www/html/apps ./owncloud_apps

build:
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true && BUILDKIT_PROGRESS=plain docker build --no-cache --progress=plain -t ${IMAGE_NAME}:${IMAGE_TAG} .

push:
	docker tag ${IMAGE_NAME}:${IMAGE_TAG} ghcr.io/theagentcompany/servers-owncloud:latest
	docker push ghcr.io/theagentcompany/servers-owncloud:latest