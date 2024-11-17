run:
	docker compose up -d
start:
	docker compose up -d
stop:
	docker compose down
rm:
	-docker volume rm owncloud_onlyoffice_data
	-docker volume rm owncloud_onlyoffice_logs
	-docker volume rm owncloud_owncloud_data
	-docker volume rm owncloud_owncloud_config
	-docker network rm owncloud_owncloud_network
restart:
	-make stop
	-make rm
	-make start