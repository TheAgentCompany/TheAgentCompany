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