# Dockerfile
FROM docker:27.3.1

# Install curl
RUN apk add --no-cache curl bash jq

# Copy backup data and script
RUN mkdir -p /backup/plane-app
COPY plane-app/* /backup/plane-app
COPY pgdata.tar.gz /backup/
COPY redisdata.tar.gz /backup/
COPY uploads.tar.gz /backup/
COPY setup.sh /backup/
COPY download.sh /backup/

# Make script executable
RUN chmod +x /backup/setup.sh
RUN chmod +x /backup/download.sh

CMD ["tail", "-f", "/dev/null"]
# ENTRYPOINT ["/restore.sh"]
# plane restore里面会开一个新的container，会有点问题