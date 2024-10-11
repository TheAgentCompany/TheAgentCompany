# How to run
Execute download.sh first

Before start, remember the default download version of `plane.env` need to be changed. You should change from `NGINX_PORT=90` into `NGINX_PORT=8091`. Then it will not conflict with nextcloud port.
 
Run `./setup.sh`, then choose `2` start. Then you will get a new cluster
See here for mored details `https://docs.plane.so/self-hosting/methods/docker-compose`

# How to backup
```
curl -fsSL -o setup.sh https://raw.githubusercontent.com/makeplane/plane/master/deploy/selfhost/install.sh

chmod +x setup.sh
```

After you launching the cluster, run `./setup.sh` and choose `7` backup data. Then you will find data in backup directory. In the directory, there will be `pgdata.tar.gz`, `redisdata.tar.gz`, and `uploads.tar.gz`

# How to restore from backup
See instruction here `https://github.com/makeplane/plane/tree/preview/deploy/selfhost#restore-data`
First make sure you already run the cluster. Then run `./setup.sh` and choose `3` stop the cluster. 
Secondly run `./restore.sh <path to backup folder containing *.tar.gz files>`
In the end, start the cluster again.

# NOTE
Follow the instruction here: https://docs.plane.so/self-hosting/methods/docker-compose
How to download the plane:
```
curl -fsSL -o setup.sh https://raw.githubusercontent.com/makeplane/plane/master/deploy/selfhost/install.sh
```
# Populated data

There is some populated data in Plane for task creators to have a starting point. This data includes:
* The company workspace name 'TheAgentCompany'
* Added 17 Employees with their relevant roles and positions within the company. 
* Each employee was assigned a username and email address based on a standard format. Password is the same as email for every employee. 

## Credentials 
Username format: `firstnamelastname` in lowercase (e.g., `emmalewis`).
Email format: `firstname.lastname@agentcompany.com` (e.g., `emma.lewis@agentcompany.com`)
Password: `firstname.lastname@agentcompany.com`(e.g., `emma.lewis@agentcompany.com`)

## Project Structure
The projects in Plane were set up to reflect the key modules of The Agent Company's core initiatives. Each module was created as a separate project to streamline organization and focus. The projects are as follows:

1. **Graph Database Project** (JanusGraph)
2. **Streaming Database Project** (RisingWave)
3. **AI Project** (OpenHands & llama.cpp)
4. **Web Crawler Project** (Colly)
5. **Search Engine Project** (OpenSearch)
6. **Low-Code Platform Project** (Node-RED)
7. **Frontend Development Project** (E-commerce Website)
8. **API Development Project** (API-server)

## Module and Issue Setup
Within each project:
- **Modules** were set up to represent key issues or tasks for that specific project.
- **Issues** were created to detail sub-issues or actionable steps necessary to complete each module's objectives.

This hierarchical structure helps break down complex tasks into manageable components, making it easier to track progress and execution.

## Sprint Cycles
Three sprint cycles have been created to manage the project timelines effectively:
1. **Sprint 1:** October 2024
2. **Sprint 2:** November 2024

Each issue was assigned to one of these sprint cycles, ensuring organized task flow and prioritization.

## Task Assignment and Distribution
### Roles and Responsibilities:
- **Database-related tasks** have been assigned to **Li Ming** and **Zhang Wei**.
- **AI and Machine Learning tasks** are handled by **Wang Fang** and **Mike Chen**.
- **Web Crawling and Distributed Systems** responsibilities are managed by **Emily Zhou**.
- **Quality Assurance** is overseen by **Liu Qiang**.
- **Product, Frontend, and API Development** tasks are distributed among **Huang Jie**, **Jessica Chen**, and **Emma Lewis**.


