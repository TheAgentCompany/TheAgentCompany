IMAGE_NAME=job-bench-pm-add-new-moderator
CONTAINER_NAME=job-bench-pm-add-new-moderator

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)