# Development Guide
This guide is for people working on JobBench and editing the source code. If you wish to contribute your changes, check out the [CONTRIBUTING.md](./CONTRIBUTING.md) on how to clone and set up the project initially before moving on. Otherwise, you can clone the JobBench project directly.

## Table of Contents

1. [Start the server for development](#start-the-server-for-development)
   1. [Requirements](#1-requirements)
   2. [Initialize parameters](#2-initialize-parameters)
   3. [Start the servers](#3-start-the-servers)
   4. [Backup and Restore](#4-backup-and-restore)
   5. [Stop the servers](#5-stop-the-servers)
2. [How to build a task image](#how-to-build-a-task-image)
   1. [Build from the base image](#1-build-from-the-base-image)
   2. [Setup the environment](#2-setup-the-environment)
   3. [Prepare the necessary file](#3-prepare-the-necessary-file)
   4. [Perform workflow inside the Docker container](#4-perform-workflow-inside-the-docker-container)
   5. [Perform partial checkpoint](#5-perform-partial-checkpoint)
      1. [TODO: How to trigger the evaluation process](#1-todo-how-to-trigger-the-evaluation-process)
      2. [Check whether file exists in image](#2-check-whether-file-exists-in-image)
      3. [TODO: Check result in GitLab, Nextcloud, Plane, Rocket.Chat](#3-todo-check-result-in-gitlab-nextcloud-plane-rocketchat)



## Start the server for development
For the internal team members, in general, you don't have to launch the server if you can visit the CMU server. We already host the service on the CMU server. If you find the service has broken down or cannot visit it, please ask @Frank Xu, @Yufan Song, or @Boxuan Li. If you want to set up the server in your own cluster, follow the instructions below.

For how to access each service, see [here](./servers/README.md)

### 1. Requirements
* Linux, Mac OS, or [WSL on Windows](https://learn.microsoft.com/en-us/windows/wsl/install)
* [Docker](https://docs.docker.com/engine/install/)

### 2. Initialize parameters
In the [Makefile](./servers/Makefile), we create several environment parameters, like below
```
GITLAB_HOME?=/home/fangzhex/ogma3/jobbench_gitlab
NEXTCLOUD_HOME?=/home/yufansong/data
HOSTNAME?=ogma.lti.cs.cmu.edu
FILE_SERVER_PORT?=8081
GITLAB_PORT?=8929
NEXTCLOUD_BACKUP_VOLUME_NAME?=nextcloud_aio_backupdir
NEXTCLOUD_BACKUP_VOLUME_PATH?=/home/yufansong/data/backup
NEXTCLOUD_IMAGE_TAG?=20240808_083748
NEXTCLOUD_PORT?=8090
```
Make sure you understand each parameter's meaning and configure it with the correct value. At the very least, you need to change the home file path, change the HOSTNAME, and ensure all ports are available on your server.

### 3. Start the servers
Execute `make start-all` in the servers directory.

For GitLab and Rocket.Chat, you can directly visit the service at the URL you configured earlier.

For Nextcloud, visit the URL, then follow the instructions to perform some manual configuration work. Currently, we have not yet figured out a good way to do it programmatically.

For Plane, you need to execute [setup.sh](./servers/plane/setup.sh), then choose "start" to launch the service.

**NOTE:** If you want to launch Plane and Nextcloud at the same time, you may need to change the web URL of Plane, or its URL will conflict with Nextcloud.

### 4. Backup and Restore
**GitLab:** TODO

**Nextcloud:** In the admin panel, you will find options to back up the data as a volume. You need to remember the password for this volume. If you want to restore, restart the service and use this volume with the password, following the instructions in the admin dashboard.

**Rocket.Chat:** After the service starts, run `backup-rocketchat` to back up the service, and run `restore-rocketchat` to restore the service.

Plane: see [here](./servers/plane/README.md) for more details.
### 4. Stop the servers
For GitLab, Nextcloud, and Rocket.Chat, you can directly execute `make stop-all` in the servers directory. This will stop all three servers.

For Plane, run [setup.sh](./servers/plane/setup.sh) and choose "stop."

## How to build a task image
If you want to create a task for benchmarking, here is an instruction on how to implement the action you want.

### 1. Build from the base image
In the [Example Dockerfile](./workspaces/tasks/example/Dockerfile), we provide a basic Dockerfile for the task image. We use Ubuntu as the base image, install the necessary packages, install Python packages, and create the workspace directory. Local files are then copied into the task image.

**NOTE:** Please try to add commands around the end of the Dockerfile whenever possible. This allows the previous layer cache to be used when building a new image, making it easier for us to review and integrate the Dockerfile.

In [Example Makefile](./workspaces/tasks/example/Makefile):
* `IMAGE_NAME` and `CONTAINER_NAME` define the task image name and container name.
* Execute `make build` to build the image. 
* Execute `make run` to run the container. 
* Execute `make stop` to stop and remove the container. 
* Execute `make attach` to run into container

### 2. Setup the envrionment
Use `RUN apt-get update && apt-get install -y {package name}` to install the linux package you want.

Use `RUN pip install {package name}` to install the python package you want.

### 3. Prepare the neccessary file
Use the following method to copy the neccessary file into docker image under `/workspace` directory.
```
COPY *py /workspace
COPY *sh /workspace
```
### 4. Perform workflow inside the Docker container
Follow the logic in [run.sh](./workspaces/tasks/example/run.sh), which is the entry point of the Docker container. Docker will execute `run.sh` when it starts. You can add anything you want here.

To execute a Python file:
1. Write the code.
2. Add a command for copying it into the `Dockerfile`.
3. Add a command for executing it in `run.sh`.

Take `initialization.sh`, `initialization.py`, `test_setup`, and `evaluator.py` as examples.

### 5. Perform partial checkpoint
Similar to the `evaluator.py`, you need to determine how to check the task you designed, either by verifying whether the final result exists or through other means.

#### 1. TODO: How to trigger the evaluation process
Currently, the `evaluator.py` is simply executed after a 10-second delay. We need to find a better way to trigger it, such as hosting a service within the task image.

#### 2. Check whether file exist in image
Check [evaluator.py](./workspaces/tasks/example/evaluator.py) function `check_code_clone` as example.

#### 3. TODO: Check result in gitlab, nextcloud, plane, rocketchat 

