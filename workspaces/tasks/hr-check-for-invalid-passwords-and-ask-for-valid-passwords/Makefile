IMAGE_NAME=hr-check-for-invalid-passwords-and-ask-for-valid-passwords-image
CONTAINER_NAME=hr-check-for-invalid-passwords-and-ask-for-valid-passwords

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