# JanusGraph Setup Guide

This guide will walk you through implementing covering index for JanusGraph.
This file is only for developers' reference and is not accessible to the examinee.

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

## Storage Backend Setup (Here needs to use cassandra)
### Step 5: Configure Cassandra
Install and configure Cassandra as the storage backend:
```bash
curl -o /etc/apt/keyrings/apache-cassandra.asc https://downloads.apache.org/cassandra/KEYS

echo "deb [signed-by=/etc/apt/keyrings/apache-cassandra.asc] [https://debian.cassandra.apache.org](https://debian.cassandra.apache.org/) 41x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list

apt-get update
apt-get install cassandra
```

Start Cassandra:
```bash
service cassandra start
```

Verify Cassandra is running (here also need to modify the CQLCompositeIndexInlinePropBenchmark.java since the datacenter name is 'datacenter1' not 'dc1'):
```bash
nodetool status
```

### Step 6: Configure host address for gremlin-server and start the janusgraph
Update `janusgraph/janusgraph-dist/target/janusgraph-full-1.1.0-SNAPSHOT/conf/gremlin-server/gremlin-server.yaml` with the following configuration:
```yaml
host: 127.0.0.1

```

Start the JanusGraph server:
```bash
./bin/janusgraph-server.sh start
```

### Step 7: Run the benchmark 
Modify the datacenter name in CQLCompositeIndexInlinePropBenchmark.java if it is needed (default is CQLConfigOptions.LOCAL_DATACENTER, "dc1")
```yaml
CQLConfigOptions.LOCAL_DATACENTER, "datacenter1"
```

Compile the file 
```bash
mvn clean install -DskipTests
cd janusgraph-benchmark
mvn dependency:copy-dependencies -DoutputDirectory=target/lib
```

Run the benchmark
```bash
java -cp "janusgraph-benchmark/target/janusgraph-benchmark-1.1.0-SNAPSHOT.jar:janusgraph-benchmark/target/lib/*:janusgraph-core/target/janusgraph-core-1.1.0-SNAPSHOT.jar" org.janusgraph.CQLCompositeIndexInlinePropBenchmark
```


### Step 8: Run all the test cases in IndexSerializerTest.java
```bash
mvn test -pl janusgraph-test -Dtest=IndexSerializerTest
```