#!/bin/bash

# Set parameters
ROOT_PATH=$(git rev-parse --show-toplevel)
CONTAINER_NAME="nextcloud-aio-nextcloud"
BACKUP_DIR=$ROOT_PATH/servers/nextcloud  # replace it with your path
BACKUP_FILENAME="nextcloud_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

# Create backup
mkdir -p "$BACKUP_DIR"

# use "docker cp" command to copy data into tmp path
TEMP_DIR=$(mktemp -d)
docker cp "$CONTAINER_NAME:/mnt/ncdata" "$TEMP_DIR"

# compress data
tar -czf "$BACKUP_DIR/$BACKUP_FILENAME" -C "$TEMP_DIR" ncdata

# clear path
rm -rf "$TEMP_DIR"

echo "data backup finish: $BACKUP_DIR/$BACKUP_FILENAME"