# Server Setup

1. Install docker, install docker compose (note: it is `docker compose`, not `docker-compose`). Make sure your linux user has the right permission to execute the docker and docker compose command. 
Install `curl`, e.g. `sudo apt install -y curl`.

2. Run `sudo chmod 666 /var/run/docker.sock` since we need to mount docker socket to the container. This is only needed for mac and linux users.

3. Execute the following command:

    <details>
      <summary>Instruction for Mac and Linux users</summary>

    ```bash
    # you should have docker and docker compose installed, and 30+ GB of free disk space
    # Mac users must have host networking enabled
    sudo chmod 666 /var/run/docker.sock
    curl -fsSL https://github.com/TheAgentCompany/the-agent-company-backup-data/releases/download/setup-script-20241208/setup.sh | sh
    ```
    </details>

    <details>
      <summary>Instruction for Windows users</summary>

    ```bash
    # you should have docker and docker compose installed, and 30+ GB of free disk space
    # you must have host networking enabled
    curl -fsSL -o setup.bat https://github.com/TheAgentCompany/the-agent-company-backup-data/releases/download/setup-script-20241208/setup.bat && setup.bat
    ```
    </details>

    The script will automatically do the following things:

    * Check your local docker and docker compose version.
    * Pull server images. Note: you need at least 30GB available storage space.
    * Start all servers and wait until they are all up and running.

4. Infra setup is finished when you see output:
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

Depending on your server's resources and network bandwidth, this might take from a few minutes to up to 30 minutes at first run.

Now you should be able to visit the services in your browser. Check out the [servers/README.md](../servers/README.md) for more details if you'd like to poke around the services.
Otherwise, ready to start evaluation? Please refer to the [EVALUATION DOC](./EVALUATION.md) for more details.

# Troubleshooting

Occasionally, you might see some service stuck in a not ready state. Server issue is usually not too concerning from evaluation
correctness perspective, as task images all contain health check logic in their initialization scripts.
They do need human intervention to recover at times. Please find common issues and troubleshooting guide below.

For reference, once all services are up and running, `docker ps` should show something like this:

<img width="1683" alt="Screenshot of all running containers" src="https://github.com/user-attachments/assets/aedf9aa1-9dfc-44e4-9ecf-b10a2e52c72a" />


## api-server waits forever (IMPORTANT)

API-server container is the controller of all services. You might see `Checking if api-server is running on port 2999...` logs
for a while (from a few minutes to 10+ minutes, depending on your server's resources) since it needs to launch all other services.

If you are using Macbook or Windows, you might see api-server waiting to launch indefinitely. In your Docker Desktop, ensure
`Settings > Resources > Network > Enable host networking` is enabled.

<img width="527" alt="Screenshot showing host networking is enabled" src="https://github.com/user-attachments/assets/3db78fee-84f6-482f-a323-cfcb256a9c92" />

On Windows, you may not see `Use kernel networking for UDP` option. Please ignore it, and make sure you have `Enable host networking` ticked.

After enabling host networking, please stop and delete all running containers and
restart Docker. Then you can run the setup script again.

## Plane not ready

We have seen cases where plane services fail to start due to some internal errors.
In this case, you can stop and remove all the containers and run the setup script again.
If the issue persists, please create a GitHub issue.

Many machines in China may face connectivity issues when trying to access GitHub or download Docker images due to network restrictions, requiring a VPN. If you're experiencing problems deploying the application, please verify the following:

1. Check if you can successfully download the Docker image
2. If you're stuck at the plane launch process, inside the `api-server` container (using `docker exec -it [container name or id] /bin/bash
`) and verify connectivity by running:

```
wget https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/docker-compose.yml
``` 

If this command fails or gets blocked, you might need to configure a VPN or proxy to establish the necessary connections for deployment.

## RocketChat not ready

If you are using Macbook M1, you might see RocketChat never ready due to failure of
`bitnami/mongodb` container, a component of RocketChat services. This is a [known issue](https://github.com/bitnami/containers/issues/40947)
with bitnami mongodb, and a workaround is to select QEMU (Legacy) or Docker VMM (BETA) as virtual machine option in Docker Desktop as follows:

<img width="823" alt="select QEMU virtual machine option in Docker Desktop" src="https://github.com/user-attachments/assets/50461290-7734-4a04-a888-bf7fc4364af9" />
