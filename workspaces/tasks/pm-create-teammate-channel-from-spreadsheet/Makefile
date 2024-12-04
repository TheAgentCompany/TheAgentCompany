IMAGE_NAME=pm-create-teammate-channel-from-spreadsheet-image
CONTAINER_NAME=pm-create-teammate-channel-from-spreadsheet

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
