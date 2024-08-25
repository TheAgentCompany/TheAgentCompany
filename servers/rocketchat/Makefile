run:
	docker compose up

stop:
	docker compose down
	docker rm rocketchat-rocketchat-1
	docker rm rocketchat-mongodb-1

clean-data:
	docker volume rm rocketchat_mongodb_data

restore:
	docker exec -i rocketchat-mongodb-1 sh -c 'mongorestore --archive' < db.dump

backup:
	docker exec rocketchat-mongodb-1 sh -c 'mongodump --archive' > db.dump
