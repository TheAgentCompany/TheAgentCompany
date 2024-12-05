IMAGE_NAME=servers-api-server-image
CONTAINER_NAME=servers-api-server
IMAGE_TAG=latest
GHCR=ghcr.io/theagentcompany
GHCR_NAME=servers-api-server

.PHONY: build run

build:
	rm -rf data
	mkdir data
	cp ../rocketchat/npc/npc_definition.json data/
	cd ../plane && make download-setup && cd -
	cp -r ../plane data/
	wget -P ./data/ https://github.com/TheAgentCompany/the-agent-company-backup-data/releases/download/rocketchat-20241123/db.dump
	cp ../rocketchat/data_restore/restore.sh data/restore.sh
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

push:
	docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${GHCR}/${GHCR_NAME}:latest
	docker push ${GHCR}/${GHCR_NAME}:latest
