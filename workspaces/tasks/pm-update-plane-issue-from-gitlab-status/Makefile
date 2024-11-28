IMAGE_NAME=pm-update-plane-issue-from-gitlab-status-image
CONTAINER_NAME=pm-update-plane-issue-from-gitlab-status

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
