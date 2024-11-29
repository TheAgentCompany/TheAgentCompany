FROM docker:27.3.1

RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    iputils \
    lsof \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers \
    make \
    bash \
    curl

# Install python package, in Alpine Linux, we cannot fix the version
RUN apk add py3-flask
RUN apk add py3-requests

RUN ln -sf python3 /usr/bin/python
ENV PYTHONPATH="/workspace:$PYTHONPATH"

# api-server
RUN mkdir -p /workspace
WORKDIR /workspace
COPY api-server.py /workspace
COPY data/docker-compose.yml /workspace/
COPY API_MAKEFILE /workspace/Makefile

# plane
RUN mkdir -p /plane/plane-app
COPY data/plane/plane-app/docker-compose.yaml /plane/plane-app
COPY data/plane/plane-app/plane.env /plane/plane-app
COPY data/plane/plane-app/restore.sh /plane/plane-app
COPY data/plane/setup.sh /plane/
COPY data/plane/download.sh /plane/
COPY data/plane/Makefile /plane/
# plane fake data, needed by restore.sh
COPY data/plane/Makefile /plane/pgdata.tar.gz
COPY data/plane/Makefile /plane/redisdata.tar.gz
COPY data/plane/Makefile /plane/uploads.tar.gz

# rocketchat
RUN mkdir /rocketchat
COPY data/db.dump /rocketchat/
COPY data/restore.sh /rocketchat/
RUN chmod 777 /rocketchat/db.dump
RUN chmod 777 /rocketchat/restore.sh

ENTRYPOINT ["tail", "-f", "/dev/null"]
