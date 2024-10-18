IMAGE_NAME=job-bench-sde-change-dependency-easy-2
CONTAINER_NAME=job-bench-change-dependency-easy-2

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)