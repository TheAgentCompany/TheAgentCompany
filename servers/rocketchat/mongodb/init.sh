#!/bin/bash
set -e

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to start..."
until mongosh --quiet --eval "db.adminCommand('ping').ok" | grep -q "1"; do
    echo "Waiting for MongoDB to start..."
    sleep 2
done

# Give MongoDB some time to fully initialize
sleep 10

echo "========= Begin to restore data ========="
# Use mongorestore without replica set configuration
mongorestore --drop --archive < /docker-entrypoint-initdb.d/db.dump

echo "========= Data restore completed ========="