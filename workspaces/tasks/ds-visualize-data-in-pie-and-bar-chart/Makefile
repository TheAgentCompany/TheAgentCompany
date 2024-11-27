IMAGE_NAME=ds-visualize-data-in-pie-and-bar-chart-image
CONTAINER_NAME=ds-visualize-data-in-pie-and-bar-chart

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash
