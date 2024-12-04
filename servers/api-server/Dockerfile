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
    curl \
    py3-pip \
    vim

RUN ln -sf python3 /usr/bin/python
ENV PYTHONPATH="/workspace:$PYTHONPATH"

# api-server
RUN mkdir -p /workspace
WORKDIR /workspace
COPY api-server.py /workspace
COPY utils.py /workspace
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
COPY data/npc_definition.json /rocketchat/
COPY data/db.dump /rocketchat/
COPY data/restore.sh /rocketchat/
RUN chmod 777 /rocketchat/db.dump
RUN chmod 777 /rocketchat/restore.sh
# For sotopia redis address, use localhost, rather than redis-stack
ENV REDIS_OM_URL redis://default:theagentcompany@localhost:6379
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN . /opt/venv/bin/activate && \
    pip install --no-cache-dir \
    rocketchat_API==1.32.0 \
    redis==5.2.0 \ 
    flask==3.1.0 \ 
    requests==2.32.3 \
    redis-om==0.3.2

ENTRYPOINT ["python", "api-server.py"]
