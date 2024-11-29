IMAGE_NAME=servers-api-server-image
CONTAINER_NAME=servers-api-server
IMAGE_TAG=latest

.PHONY: build run

build:
	rm -rf data
	mkdir data
	cp ../../docker-compose.yml data/
	cd ../../plane && make download-setup
	cp -r ../../plane data/
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true && docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --rm -d \
		--network host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--name $(CONTAINER_NAME) $(IMAGE_NAME)

run-tail:
	docker run --rm -d \
		--network host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--name $(CONTAINER_NAME) $(IMAGE_NAME) \
		tail -f /dev/null

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

attach:
	docker exec -it $(CONTAINER_NAME) sh

