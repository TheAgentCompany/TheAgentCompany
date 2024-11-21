# This readme is for developer's reference only, not for the examinees
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

### Step 5: Modify the host in conf/gremlin-server/gremlin-server.yaml
```bash
host:127.0.0.1
```

### Step 6: Start the Janusgraph database
```bash
./bin/janusgraph-server.sh start

./bin/janusgraph-server.sh status
```

### Step 7: Start the Gremlin Console and connect to remote server
```bash
cd bin
./gremlin.sh
:remote connect tinkerpop.server conf/remote.yaml
:remote console
```

### Step 8: Create all the data based on the employee_diagram
```bash
// Create all the employee
sarah = g.addV('person').property('name', 'Sarah Johnson').property('title', 'CTO').next()

mike = g.addV('person').property('name', 'Mike Chen').property('title', 'Senior Software Engineer').next()

zhang = g.addV('person').property('name', 'Zhang Wei').property('title', 'Senior Software Engineer').next()

wang = g.addV('person').property('name', 'Wang Fang').property('title', 'AI Researcher').next()

li = g.addV('person').property('name', 'Li Ming').property('title', 'Database Project Manager').next()

emily = g.addV('person').property('name', 'Emily Zhou').property('title', 'Software Engineer').next()

emma = g.addV('person').property('name', 'Emma Lewis').property('title', 'Software Engineer').next()

alex = g.addV('person').property('name', 'Alex Turner').property('title', 'Software Engineer').next()

// Create specific relationship

g.V().has('name', 'Mike Chen').addE('reports_to').to(V().has('name', 'Sarah Johnson'))
g.V().has('name', 'Zhang Wei').addE('reports_to').to(V().has('name', 'Sarah Johnson'))
g.V().has('name', 'Wang Fang').addE('reports_to').to(V().has('name', 'Sarah Johnson'))
g.V().has('name', 'Li Ming').addE('reports_to').to(V().has('name', 'Sarah Johnson'))

g.V().has('name', 'Emily Zhou').addE('reports_to').to(V().has('name', 'Mike Chen'))
g.V().has('name', 'Emma Lewis').addE('reports_to').to(V().has('name', 'Mike Chen'))

g.V().has('name', 'Alex Turner').addE('reports_to').to(V().has('name', 'Zhang Wei'))


```