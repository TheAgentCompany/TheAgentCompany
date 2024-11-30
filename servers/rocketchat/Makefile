run:
	docker compose up

stop:
	docker compose down
	docker rm servers-rocketchat-1
	docker rm rocketchat-mongodb

clean-data:
	docker volume rm servers_mongodb_data

restore:
	docker exec -i rocketchat-mongodb sh -c 'mongorestore --archive' < db.dump

backup:
	docker exec rocketchat-mongodb sh -c 'mongodump --archive' > db.dump
