# Server: nextcloud
## Starting up server
```
export NEXTCLOUD_HOME=/home/fangzhex/ogma3/jobbench_nextcloud
docker compose up -d
docker ps
# Some useful command
# create volume for backup, remeber change the device path
# the name nextcloud_aio_backupdir is suggested by official doc, if you don't know what it is, keep it unchange.
docker volume create \
    --driver local \
    --name nextcloud_aio_backupdir \
    -o device="/home/yufansong/data/backup" \
    -o type="none" \
    -o o="bind"


# remove and delete nextcloud related docker
docker ps -q --filter "name=nextcloud" | xargs -r docker stop 
docker ps -a -q --filter "name=nextcloud" | xargs -r docker rm
# delete the volume related to nextcloud excpet for backup volume
docker volume ls -q --filter "name=nextcloud" | grep -v "nextcloud_aio_backupdir" | xargs -r docker volume rm

docker exec -it nextcloud-aio-mastercontainer /bin/bash
# get the configruation of nextcloud
docker exec nextcloud-aio-mastercontainer cat /mnt/docker-aio-config/data/configuration.json
```
Instruction about how to reset the nextcloud:
https://github.com/nextcloud/all-in-one#how-to-properly-reset-the-instance

## remember use the correct port
visit https://ogma.lti.cs.cmu.edu:8090

## Import data

Check out `gitlab_import` directory.


## NextCloud
* service url: https://ogma.lti.cs.cmu.edu/login
* username: admin
* password: 
    * If you use the backup in server: `e42a78e0ca1ca798d98827946cb271cb9e428d357069d547`
    * else try `make get-nextcloud-config` then check `secrets.NEXTCLOUD_PASSWORD`
* admin panel: https://ogma.lti.cs.cmu.edu:8090/
* backup: 
    * volume name: nextcloud_aio_backupdir
    * password: d352748d4845e6a70d0517c568b879d1e3dba54deb0b7e6c
