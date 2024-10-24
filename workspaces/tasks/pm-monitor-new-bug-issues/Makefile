IMAGE_NAME=pm-monitor-new-bug-issues-image
CONTAINER_NAME=pm-monitor-new-bug-issues-image

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)