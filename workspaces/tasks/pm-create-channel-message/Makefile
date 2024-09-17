IMAGE_NAME=job-bench-pm-create-channel-message-image
CONTAINER_NAME=job-bench-pm-create-channel-message

.PHONY: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)