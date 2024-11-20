IMAGE_NAME=servers-rocketchat-npc-data-population-image
CONTAINER_NAME=servers-rocketchat-npc-data-population

.PHONY: build run

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run -d --name $(CONTAINER_NAME) $(IMAGE_NAME)
	docker logs $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash
