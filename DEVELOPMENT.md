# Development Guide

Target audience: benchmark developers.

TODO: polish the doc and remove CMU internal guidelines before public release.
TODO: some content in this doc is actually user doc rather than dev doc. We need to split them.

If you wish to contribute your changes, check out the [CONTRIBUTING.md](./CONTRIBUTING.md) on how to clone and set up the project initially before moving on. Otherwise, you can clone TheAgentCompany project directly.

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
HOSTNAME?=ogma.lti.cs.cmu.edu
FILE_SERVER_PORT?=8081
GITLAB_PORT?=8929
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

### 5. Stop the servers
For GitLab, Nextcloud, and Rocket.Chat, you can directly execute `make stop-all` in the servers directory. This will stop all three servers.

For Plane, run [setup.sh](./servers/plane/setup.sh) and choose "stop."

## How to build a task image
If you want to create a task for benchmarking, please read [this](./workspaces/tasks/example/README.md).

