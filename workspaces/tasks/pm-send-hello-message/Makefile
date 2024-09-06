IMAGE_NAME=job-bench-pm-send-hello-message-image
CONTAINER_NAME=job-bench-pm-send-hello-message

.PHONY: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash