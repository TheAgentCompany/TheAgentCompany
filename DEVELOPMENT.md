# Development Guide
This guide is for people working on JobBench and editing the source code. If you wish to contribute your changes, check out the [CONTRIBUTING.md](./CONTRIBUTING.md) on how to clone and setup the project initially before moving on. Otherwise, you can clone the JobBench project directly.

## Table of Contents

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
   4. [Do workflow inside the docker when running](#4-do-workflow-inside-the-docker-when-running)
   5. [Do partial checkpoint](#5-do-partial-checkpoint)
      1. [TODO: How to trigger the evaluation process](#1-todo-how-to-trigger-the-evaluation-process)
      2. [Check whether file exists in image](#2-check-whether-file-exists-in-image)
      3. [TODO: Check result in GitLab, NextCloud, Plane, RocketChat](#3-todo-check-result-in-gitlab-nextcloud-plane-rocketchat)



## Start the server for development
For the internal team members, in general, you don't have to launch server if you can visit the CMU server. We already host the service in CMU server. If you find service break down or cannot visit, please ask @Frank Xu, @Yufan Song or @Boxuan Li. If you want to setup the server in your own cluster, follow the instructions below.

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
Make sure you understand each parameter's meaning and config it into correct value. At lease, you need to change the home file path, change the HOSTNAME, make all ports are available in your server.

### 3. Start the servers
Execute `make start-all` in servers directory.

For gitlab and rocketchat, you can directly visit the service in the url you configured before.

For nextcloud, visit the url, then it should follow the instruction to do some manually configuration work. Currently we still not figure out a good way to do it programmatically.

For plane, you need to execute [setup.sh](./servers/plane/setup.sh), then choose start to launch the service. 

NOTE: If you want to launch plane and nextcloud at the same time, you may need to change the web url of plane, or it's url will conflict with nextcloud.

### 4. Backup and Restore
Gitlab: TODO

NextCloud: in the admin panel of it, it shows the options to backup the data as a volume, and you need to remember the password for this volume. If you want to restore, restart the service and use this volume with password follow the instruction in admin dashboard. 

RocketChat: after the service start, run `backup-rocketchat` to backup the service, run `restore-rocketchat` to start the service.

Plane: see [here](./servers/plane/README.md) for more details.

### 4. Stop the servers
For gitlab, nextcloud, and rocketchat, you can directly execute `make stop-all` in servers directory. Then these three servers will stop. 

For Plane, run [setup.sh](./servers/plane/setup.sh) and choose stop.


## How to build a task image
If you want to create one task for benchmark, here is a instruction about how to implement the action you want.

### 1. Build from the base image
In [Example Dockerfile](./workspaces/tasks/example/Dockerfile), we provide the basic Dockerfile for task image. We use the ubuntu as the base image, install the neccesary package, install python package, create the workspace directory. Copy local file into the task image.

NOTE: Please try to add command around the end of dockerfile if possible, then the previous layer cache can be used when build new image. And it make us easier to review and integration the dockerfile.

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

### 4. Do workflow inside the docker when running
Follow the logic in [run.sh](./workspaces/tasks/example/run.sh), this is the entry point of the docker. Docker will execute the `run.sh` when start. You can add anything you want here.

execute the python file
1. write code
2. add command for copying it into `Dockerfile`
3. add command for executing it in `run.sh`

Taks `update_hosts.sh`, `functionality.py` and `evaluator.py` as the example.

### 5. Do partial checkpoint
Like the `evaluator.py`, you need to figure out how to check the task you design by check whether final result exist or in other way.

#### 1. TODO: How to trigger the evaluation process
Currently just simply execute the `evaluator.py` after 10s. Need to figure out a better way to trigger it for example host a service in task image.

#### 2. Check whether file exist in image
Check [evaluator.py](./workspaces/tasks/example/evaluator.py) function `check_code_clone` as example.

#### 3. TODO: Check result in gitlab, nextcloud, plane, rocketchat 

