IMAGE_NAME=servers-plane-restore-image
CONTAINER_NAME=servers-plane-restore
IMAGE_TAG=latest

download-setup:
	sh ./download.sh
	curl -fsSL -o setup.sh https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/install.sh
	chmod +x setup.sh
	chmod 777 setup.sh

rm-plane-volume:
	docker volume ls -q --filter "name=plane-app" | xargs -r docker volume rm

start-plane: download-setup
	./setup.sh start
	make reset-plane

start-plane-without-data:
	./setup.sh start

reset-plane:
	make stop-plane
	./plane-app/restore.sh ./
	make start-plane-without-data

stop-plane:
	./setup.sh stop

backup-plane:
	./setup.sh backup

.PHONY: build run

build:
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

