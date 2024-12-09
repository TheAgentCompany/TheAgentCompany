# Setup Infra

1. Install docker, install docker compose (note: it is `docker compose`, not `docker-compose`). Make sure your linux user has the right permission to execute the docker and docker compose command. 
Install `curl`, e.g. `sudo apt install -y curl`.

2. Run `sudo chmod 666 /var/run/docker.sock` since we need to mount docker socket to the container.

3. Execute the following command:
```
curl -fsSL https://github.com/TheAgentCompany/the-agent-company-backup-data/releases/download/setup-script-20241208/setup.sh | sh
```
It will automatically do the following things:

* Check your local docker and docker compose version.
* Pull image. Actually the image will auto pull in the next step, but the image is pretty large, around 15GB. Better pull it here to check for correctness. 
* Wait 120s for service launching until you pass the next step 
* Check whether service up.

4. Infra setup finished when you see output:
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

# Setup Evaluation
If you need to use OpenHands for evaluation, you also need:
1. python 3.12
2. poetry
3. install dependencies using `poetry install` under project root directory
4. docker buildx
