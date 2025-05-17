FROM ghcr.io/li-boxuan/task-base-image:1.0.0

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      postgresql-client