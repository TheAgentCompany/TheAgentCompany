# Setup Infra

1. install docker, install docker compose (note: it is `docker compose`, not `docker-compose`). Make sure your linux user has the right permission to execute the docker and docker compose command. 
Install `make` and `curl`, e.g. `sudo apt install -y curl make`.

2. Run `sudo chmod 666 /var/run/docker.sock` since we need to mount docker socket to the container.
Check the installation by goto servers directory and run `make check`. The command should show your local docker and docker compose version.

3. Goto servers directory and run `make setup`. It will automatically do the following things:
    * Pull image by `make pull-image`. Actually the image will auto pull in the next step, but the image is pretty large, around 15GB. Better pull it here to check for correctness. 
    * Run `make start-api-server-with-setup` and wait 60s for service launching until you pass the next step 
    * Run `make health-check` to check whether service up.

4. When you see output:
```
Checking if api-server is running on port 2999...
api-server is running on port 2999!
Starting health checks...
rocketchat is ready!
owncloud is ready!
gitlab is ready!
plane is ready!
All services are up and running!
```
infra setup finished.

# Setup Evaluation
If you need to use OpenHands for evaluation, you also need:
1. python 3.12
2. poetry
3. install dependencies using `poetry install` under project root directory
4. docker buildx
