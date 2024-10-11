run:
	docker compose up

stop:
	docker compose down
	docker rm servers-rocketchat-1
	docker rm servers-mongodb-1

clean-data:
	docker volume rm servers_mongodb_data

restore:
	docker exec -i servers-mongodb-1 sh -c 'mongorestore --archive' < db.dump

backup:
	docker exec servers-mongodb-1 sh -c 'mongodump --archive' > db.dump
