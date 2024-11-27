IMAGE_NAME=sde-copilot-arena-server-easy-add-suffix-image
CONTAINER_NAME=sde-copilot-arena-server-easy-add-suffix

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
