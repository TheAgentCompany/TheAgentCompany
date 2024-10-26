get-set:
	curl -fsSL -o setup.sh https://raw.githubusercontent.com/makeplane/plane/master/deploy/selfhost/install.sh
	chmod +x setup.sh

rm-plane-volume:
	docker volume ls -q --filter "name=plane-app" | xargs -r docker volume rm

start-plane:
	sh ./download.sh
	chmod 777 setup.sh
	./setup.sh start

stop-plane:
	./setup.sh stop

backup-plane:
	./setup.sh backup