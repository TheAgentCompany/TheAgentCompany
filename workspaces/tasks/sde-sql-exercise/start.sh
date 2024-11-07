#!/bin/bash

echo "Initializing SQLite database..."

if [ ! -f /data/database.db ]; then
    echo "Creating new SQLite database..."
    sqlite3 /data/database.db < /data/init.sql
fi

exec "$@"