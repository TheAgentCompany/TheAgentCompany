# How to run
Execute download.sh first

Before start, remember the default download version of `plane.env` need to be changed. You should change from `NGINX_PORT=90` into `NGINX_PORT=8091`. Then it will not conflict with nextcloud port.
 
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
