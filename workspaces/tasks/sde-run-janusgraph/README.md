# JanusGraph Setup Guide

This guide will walk you through setting up JanusGraph with HTTP endpoint support.

## Prerequisites Installation
### Step 1: Install Java 11 and Maven
```bash
apt-get update
apt-get install zip
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 11.0.25-zulu
apt install maven
```

## JanusGraph Setup
### Step 2: Clone and Configure JanusGraph
Clone the JanusGraph repository and follow [this PR](https://github.com/JanusGraph/janusgraph/pull/4694/files) to skip the docker-in-docker build.

### Step 3: Build Binary
Build the JanusGraph binary with the following command (with skipdocker):
```bash
mvn clean install -Pjanusgraph-release -Dgpg.skip=true -DskipTests=true -Pskip-docker
```

### Step 4: Verify and Extract Binary
Check if the binary (janusgraph-dist/target/janusgraph-$VERSION.zip) exists and extract it:
```bash
unzip janusgraph-full-1.1.0-SNAPSHOT.zip
```

## Storage Backend Setup (Here I use the HBase)
### Step 5: Configure HBase and Java Environment
Install and configure HBase as the storage backend:
```bash
wget https://archive.apache.org/dist/hbase/2.5.5/hbase-2.5.5-bin.tar.gz
tar xzf hbase-2.5.5-bin.tar.gz
cd hbase-2.5.5
```

Configure Java environment in `~/.bashrc`:
```bash
export JAVA_HOME="/root/.sdkman/candidates/java/current"
export PATH=$JAVA_HOME/bin:$PATH
source ~/.bashrc
```

Start HBase:
```bash
./bin/start-hbase.sh
```

## HTTP Endpoint Configuration
### Step 6: Configure HTTP Endpoint
Update `http-gremlin-server.yaml` with the following configuration [reference](https://docs.janusgraph.org/operations/server/#janusgraph-server-as-a-http-endpoint):
```yaml
host: 127.0.0.1
channelizer: org.apache.tinkerpop.gremlin.server.channel.HttpChannelizer
graphs: { 
    graph: conf/gremlin-server/http-janusgraph-hbase-server.properties
}
```

Start the JanusGraph server:
```bash
bin/janusgraph-server.sh console ./conf/gremlin-server/http-gremlin-server.yaml
```

### Step 7: Verify HTTP Server with 200 status code and 
Test the HTTP endpoint:
```bash
curl -XPOST -Hcontent-type:application/json -d '{"gremlin":"g.V().count()"}' http://127.0.0.1:8182
```