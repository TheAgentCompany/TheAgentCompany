IMAGE_NAME=base-image
CONTAINER_NAME=base-image

.PHONY: build run

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run -d --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash
