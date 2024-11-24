IMAGE_NAME=ds-calculate-spreadsheet-stats-image
CONTAINER_NAME=ds-calculate-spreadsheet-stats

.PHONY: build run stop attach

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --network host --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash