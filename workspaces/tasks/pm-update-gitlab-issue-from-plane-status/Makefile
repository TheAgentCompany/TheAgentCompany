IMAGE_NAME=pm-update-gitlab-issue-from-plane-status-image
CONTAINER_NAME=pm-update-gitlab-issue-from-plane-status

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
