IMAGE_NAME=sde-implement-buffer-pool-manager-bustub-image
CONTAINER_NAME=sde-implement-buffer-pool-manager-bustub

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
