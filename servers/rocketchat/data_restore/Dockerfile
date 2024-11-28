# Dockerfile
FROM docker:27.3.1

# Install curl
RUN apk add --no-cache curl

# Copy backup data and script
COPY db.dump /backup/db.dump
COPY restore.sh /restore.sh

# Make script executable
RUN chmod +x /restore.sh

ENTRYPOINT ["/restore.sh"]