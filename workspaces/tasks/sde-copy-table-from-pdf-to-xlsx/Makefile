IMAGE_NAME=sde-copy-table-from-pdf-to-xlsx-image
CONTAINER_NAME=sde-copy-table-from-pdf-to-xlsx

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash 

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
