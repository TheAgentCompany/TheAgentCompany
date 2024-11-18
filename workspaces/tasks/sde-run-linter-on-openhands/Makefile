IMAGE_NAME=sde-run-linter-on-openhands-image
CONTAINER_NAME=sde-run-linter-on-openhands

.PHONY: build run stop attach

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --privileged --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash
