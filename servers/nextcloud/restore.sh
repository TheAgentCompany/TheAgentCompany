#!/bin/bash

# set parameters
CONTAINER_NAME="nextcloud-aio-nextcloud"
ROOT_PATH=$(git rev-parse --show-toplevel)
BACKUP_FILE=$ROOT_PATH/servers/nextcloud/nextcloud_backup_20240930_000504.tar.gz  # replace it with your backup file

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