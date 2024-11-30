#!/bin/sh

MAX_ATTEMPTS=300
SLEEP_INTERVAL=2

check_rocketchat() {
    # Using curl to check if RocketChat is accessible
    curl -s -o /dev/null -w "%{http_code}" "localhost:3000/api/info"
}


# Keep trying until RocketChat is available
attempt=1
while [ $attempt -le $MAX_ATTEMPTS ]; do
    echo "Attempt $attempt of $MAX_ATTEMPTS: Checking RocketChat availability..."
    
    status_code=$(check_rocketchat)
    
    if [ "$status_code" = "200" ]; then
        echo "RocketChat is available. Starting MongoDB restore..."
        docker exec -i rocketchat-mongodb sh -c 'mongorestore --drop --archive' < /rocketchat/db.dump
        exit 0
    fi
    
    echo "RocketChat not available (status code: $status_code). Waiting $SLEEP_INTERVAL seconds..."
    sleep $SLEEP_INTERVAL
    attempt=$((attempt + 1))
done

echo "Failed to connect to RocketChat after $MAX_ATTEMPTS attempts"
exit 1