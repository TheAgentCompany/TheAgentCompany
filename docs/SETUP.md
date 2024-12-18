# Server Setup

1. Install docker, install docker compose (note: it is `docker compose`, not `docker-compose`). Make sure your linux user has the right permission to execute the docker and docker compose command. 
Install `curl`, e.g. `sudo apt install -y curl`.

2. Run `sudo chmod 666 /var/run/docker.sock` since we need to mount docker socket to the container.

3. Execute the following command:
```
curl -fsSL https://github.com/TheAgentCompany/the-agent-company-backup-data/releases/download/setup-script-20241208/setup.sh | sh
```
It will automatically do the following things:

* Check your local docker and docker compose version.
* Pull server images. Note: you need at least 30GB available storage space.
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

Now you are ready to start evaluation. Please refer to the [EVALUATION DOC](./EVALUATION.md) for more details.

# Troubleshooting

Occasionally, you might see some service stuck in a not ready state.
We have seen cases where plane services fail to start due to some internal errors.
In this case, you can stop and remove all the containers and run the setup script again.
If the issue persists, please create a GitHub issue.

Note: server issue is usually not too concerning from evaluation correctness perspective, as task
images all contain health check logic in their initialization scripts.