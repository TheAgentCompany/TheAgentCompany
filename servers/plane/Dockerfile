# Dockerfile
FROM docker:27.3.1

# Install curl
RUN apk add --no-cache curl bash jq

# Copy backup data and script
RUN mkdir -p /plane/plane-app
COPY plane-app/* /plane/plane-app
COPY pgdata.tar.gz /plane/
COPY redisdata.tar.gz /plane/
COPY uploads.tar.gz /plane/
COPY setup.sh /plane/
COPY download.sh /plane/

# Make script executable
RUN chmod +x /plane/setup.sh
RUN chmod +x /plane/download.sh

ENTRYPOINT ["/plane/plane-app/restore.sh"]