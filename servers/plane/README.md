# How to run
Run `./setup.sh`, then choose `2` start. Then you will get a new cluster
See here for mored details `https://docs.plane.so/self-hosting/methods/docker-compose`

# How to backup
After you launching the cluster, run `./setup.sh` and choose `7` backup data. Then you will find data in backup directory. In the directory, there will be `pgdata.tar.gz`, `redisdata.tar.gz`, and `uploads.tar.gz`

# How to restore from backup
See instruction here `https://github.com/makeplane/plane/tree/preview/deploy/selfhost#restore-data`
First make sure you already run the cluster. Then run `./setup.sh` and choose `3` stop the cluster. 
Secondly run `./restore.sh <path to backup folder containing *.tar.gz files>`
In the end, start the cluster again.

# NOTE
Follow the instruction here: https://docs.plane.so/self-hosting/methods/docker-compose
How to download the plane:
```
curl -fsSL -o setup.sh https://raw.githubusercontent.com/makeplane/plane/master/deploy/selfhost/install.sh
```

# TODO
Solve the licence problem
1. Remove `setup.sh` file from a fix version url, change it into curl command
2. Remove `docker-compose.yaml` Replace the ${APP_RELEASE:-stable} in dockerfile, may need to figure out the how to set the `web_url`
3. Remove `restore.sh`, let user download it via `setup.sh`