IMAGE_NAME=servers-rocketchat-npc-data-population-image
CONTAINER_NAME=servers-rocketchat-npc-data-population

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
	make build
	docker tag servers-rocketchat-npc-data-population-image:latest ghcr.io/theagentcompany/servers-rocketchat-npc-data-population:latest
	docker push ghcr.io/theagentcompany/servers-rocketchat-npc-data-population:latest
