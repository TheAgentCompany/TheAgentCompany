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

start-plane-without-data: download-setup
	./setup.sh start

reset-plane:
	make stop-plane
	./plane-app/restore.sh ./
	make start-plane-without-data

stop-plane:
	./setup.sh stop

backup-plane:
	./setup.sh backup