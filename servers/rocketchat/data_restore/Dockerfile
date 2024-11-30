# Dockerfile
FROM docker:27.3.1

# Install curl
RUN apk add --no-cache curl

# Copy backup data and script
RUN mkdir /rocketchat
COPY db.dump /rocketchat/db.dump
COPY restore.sh /restore.sh

# Make script executable
RUN chmod +x /restore.sh

ENTRYPOINT ["/restore.sh"]