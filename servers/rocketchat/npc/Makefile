IMAGE_NAME=servers-rocketchat-npc-data-population-image
CONTAINER_NAME=servers-rocketchat-npc-data-population
IMAGE_TAG=latest
GHCR=ghcr.io/theagentcompany
GHCR_NAME=servers-rocketchat-npc-data-population

.PHONY: build run

build:
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true && docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run -d --name $(CONTAINER_NAME) $(IMAGE_NAME)
	docker logs $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash

push:
	docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${GHCR}/${GHCR_NAME}:latest
	docker push ${GHCR}/${GHCR_NAME}:latest
