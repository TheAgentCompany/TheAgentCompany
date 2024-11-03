IMAGE_NAME=pm-copy-plane-issues-to-gitlab-image
CONTAINER_NAME=pm-copy-plane-issues-to-gitlab-status

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
