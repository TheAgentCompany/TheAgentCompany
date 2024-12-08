# Setup Infra

1. install docker, install docker compose (note: it is `docker compose`, not `docker-compose`). Make sure your linux user has the right permission to execute the docker and docker compose command. 
Install `make`, e.g. `sudo apt install make.

2. Run `sudo chmod 666 /var/run/docker.sock` since we need to mount docker socket to the container.
Check the installation by goto servers directory and run [`make check`](../servers/Makefile#L197). The command should show your local docker and docker compose version.

3. Pull image by [`make pull-image`](../servers/Makefile#L177) . Actually the image will auto pull in the next step, but the image is pretty large, around 15GB. Better pull it here to check for correctness. 

4. Run [`make setup`](../servers/Makefile#L151) and wait until you pass the next step 

5. Run [`make health-check`](../servers/Makefile#L203) to check whether service up.
Setup finished.

# Setup Evaluation
If you need to use OpenHands for evaluation, you also need:
1. python 3.12
2. poetry
3. install dependencies using `poetry install` under project root directory
4. docker buildx
