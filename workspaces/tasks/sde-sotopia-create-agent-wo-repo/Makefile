IMAGE_NAME=sde-sotopia-create-agent-wo-repo-image
CONTAINER_NAME=sde-sotopia-create-agent-wo-repo

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash -c "/utils/init.sh && /bin/bash"

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)