IMAGE_NAME=pm-ask-issue-assignee-for-issue-status-and-update-in-plane-image
CONTAINER_NAME=pm-ask-issue-assignee-for-issue-status-and-update-in-plane

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
