IMAGE_NAME=hr-check-attendance-multiple-days-department-2-image
CONTAINER_NAME=hr-check-attendance-multiple-days-department-2

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)