FROM ghcr.io/li-boxuan/task-base-image:1.0.0

# install sqlite3
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data
COPY init.sql /data/

# init the table
RUN sqlite3 /data/database.db < /data/init.sql