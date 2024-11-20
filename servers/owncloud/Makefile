run:
	docker compose up -d
start:
	docker compose up -d
stop:
	docker compose down
rm:
	-docker network rm owncloud_owncloud_network
restart:
	-make stop
	-make rm
	-make start
	-docker exec -it owncloud bash

build:
	docker rmi owncloud:test || true && BUILDKIT_PROGRESS=plain docker build --no-cache --progress=plain -t owncloud:test .

push:
	docker tag owncloud:test ghcr.io/theagentcompany/servers-owncloud:latest
	docker push ghcr.io/theagentcompany/servers-owncloud:latest