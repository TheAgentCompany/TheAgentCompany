IMAGE_NAME=sde-close-all-issue-on-all-project-under-tac-workspace-image
CONTAINER_NAME=sde-close-all-issue-on-all-project-under-tac-workspace

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash
