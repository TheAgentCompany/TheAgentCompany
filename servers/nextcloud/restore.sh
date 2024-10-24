#!/bin/bash

# set parameters
CONTAINER_NAME="nextcloud-aio-nextcloud"
ROOT_PATH=$(git rev-parse --show-toplevel)
# use latest backup
BACKUP_FILE=$(ls -t $ROOT_PATH/servers/nextcloud/nextcloud_backup_*.tar.gz | head -n1)

# check whether file exist
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: back up file not exist"
    exit 1
fi

# create tmp path and unzip the backup file
TEMP_DIR=$(mktemp -d)
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# use "docker cp" command to unzip the data into container
docker cp "$TEMP_DIR/ncdata/." "$CONTAINER_NAME:/mnt/ncdata"

# remove tmp folder
rm -rf "$TEMP_DIR"

echo "data restore finished!"