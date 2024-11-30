IMAGE_NAME=servers-rocketchat-restore-image
CONTAINER_NAME=servers-rocketchat-restore
IMAGE_TAG=latest
GHCR=ghcr.io/theagentcompany
GHCR_NAME=servers-rocketchat-restore

.PHONY: build run

build:
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true && docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --rm -d \
		--network host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--name $(CONTAINER_NAME) $(IMAGE_NAME)
	docker logs $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash

push:
	docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${GHCR}/${GHCR_NAME}:latest
	docker push ${GHCR}/${GHCR_NAME}:latest
