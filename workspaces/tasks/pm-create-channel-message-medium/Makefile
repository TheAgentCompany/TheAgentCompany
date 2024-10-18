IMAGE_NAME=job-bench-pm-create-channel-message-medium-image
CONTAINER_NAME=job-bench-pm-create-channel-medium-message

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)