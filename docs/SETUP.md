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

Now you should be able to visit the services in your browser. Check out the [servers/README.md](../servers/README.md) for more details if you'd like to poke around the services.
Otherwise, ready to start evaluation? Please refer to the [EVALUATION DOC](./EVALUATION.md) for more details.

# Troubleshooting

Occasionally, you might see some service stuck in a not ready state. Server issue is usually not too concerning from evaluation
correctness perspective, as task images all contain health check logic in their initialization scripts.

## Plane not ready

We have seen cases where plane services fail to start due to some internal errors.
In this case, you can stop and remove all the containers and run the setup script again.
If the issue persists, please create a GitHub issue.

## RocketChat not ready

If you are using Macbook M1, you might see RocketChat never ready due to failure of
`bitnami/mongodb` container, a component of RocketChat services. This is a [known issue](https://github.com/bitnami/containers/issues/40947)
with bitnami mongodb, and a workaround is to select QEMU as virtual machine option in Docker Desktop as follows:

<img width="823" alt="Screenshot 2024-12-28 at 3 14 48 PM" src="https://github.com/user-attachments/assets/50461290-7734-4a04-a888-bf7fc4364af9" />
