FROM docker.io/bitnami/mongodb:5.0

# Copy backup data and initialization script with correct permissions
COPY --chown=1001:1001 ./db.dump /docker-entrypoint-initdb.d/
COPY --chown=1001:1001 --chmod=755 ./init.sh /docker-entrypoint-initdb.d/