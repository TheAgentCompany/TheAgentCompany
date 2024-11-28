IMAGE_NAME=ds-fix-table-values-and-missing-answers-image
CONTAINER_NAME=ds-fix-table-values-and-missing-answers

.PHONY: build run stop attach

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash