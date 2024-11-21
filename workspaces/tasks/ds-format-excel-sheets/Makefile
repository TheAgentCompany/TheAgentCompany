IMAGE_NAME=ds-format-excel-sheets-image
CONTAINER_NAME=ds-format-excel-sheets

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) . --no-cache

run:
	docker run --name $(CONTAINER_NAME) -it $(IMAGE_NAME) /bin/bash -c "/utils/init.sh && /bin/bash"

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)