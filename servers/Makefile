SHELL = /bin/bash

GITLAB_HOME?=/home/fangzhex/ogma3/jobbench_gitlab
NEXTCLOUD_HOME?=/home/fangzhex/ogma3/jobbench_nextcloud
HOSTNAME?=ogma.lti.cs.cmu.edu
FILE_SERVER_PORT?=8081

.PHONY: init start-all stop-all start-nextcloud stop-nextcloud start-file-server stop-file-server start-gitlab stop-gitlab gitlab-root-password

init:
	$(eval export GITLAB_HOME)
	$(eval export NEXTCLOUD_HOME)
	$(eval export HOSTNAME)

start-all: init
	docker compose up

stop-all:
	docker compose down

start-nextcloud:
	cd nextcloud && docker compose up -d

stop-nextcloud:
	cd nextcloud && docker compose down

start-file-server:
	cd static && python3 -m http.server 8081 -d files/ &

stop-file-server:
	@echo "Killing process on port $(FILE_SERVER_PORT)"
	@lsof -ti :$(FILE_SERVER_PORT) | xargs kill -9 || echo "No process found on port $(FILE_SERVER_PORT)"

start-gitlab: init
	docker compose up gitlab

stop-gitlab:
	docker compose down gitlab

gitlab-root-password:
	docker exec -it gitlab bash -c "grep -oP 'Password:\s*\K\S+' /etc/gitlab/initial_root_password"
