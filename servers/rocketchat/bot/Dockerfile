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

# Please keep above command unchange unless necessary.
# Add change below.

# Install Python requests library
RUN pip install requests
RUN pip install rocketchat_API==1.32.0
RUN pip install sotopia==0.1.0-rc.1

COPY *.json  /workspace
COPY *.py /workspace

# Docker bridge network: 172.17.0.1
ENV REDIS_OM_URL redis://default:jobbench@172.17.0.1:8092
# ENV OPENAI_API_KEY <Your OPENAI_API_KEY>

# keep the container running (optional)
CMD python main.py