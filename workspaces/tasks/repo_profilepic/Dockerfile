FROM ubuntu:22.04

# install basic packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    unzip \
    zip \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    openssh-server \
    sudo \
    gcc \
    jq \
    g++ \
    make \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p -m0755 /var/run/sshd

# symlink python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python

# create workspace and related files
RUN mkdir -p /workspace

# set the working directory
WORKDIR /workspace

# COPY file into working directory
COPY *py /workspace
COPY *sh /workspace

# keep the container running
CMD ["tail", "-f", "/dev/null"]