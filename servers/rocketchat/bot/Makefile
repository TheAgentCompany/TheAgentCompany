IMAGE_NAME=job-bench-rocketchat-bot
CONTAINER_NAME=job-bench-rocketchat-bot

.PHONY: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --network host --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) /bin/bash