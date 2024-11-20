IMAGE_NAME=mongodb
IMAGE_TAG=test

run:
	docker compose up -d
start:
	docker compose up -d
stop:
	docker compose down
rm:
	docker volume rm mongodb_data
restart:
	-make stop
	-make rm
	-make start
	-docker exec -it ${IMAGE_NAME} bash

build:
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true && BUILDKIT_PROGRESS=plain docker build --no-cache --progress=plain -t ${IMAGE_NAME}:${IMAGE_TAG} .
