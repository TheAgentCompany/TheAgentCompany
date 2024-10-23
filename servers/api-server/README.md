# API SERVER

Remeber to do `/etc/host` change in [here](../README.md). Or you need to replace all `the-agent-company.com` with `ogma.lti.cs.cmu.edu` in the following commands.

```bash
# Get nextcloud login password
curl http://the-agent-company.com:2999/api/nextcloud-config

# Reset the data of RocketChat to default. It may take ~1 minutes
curl -X POST http://the-agent-company.com:2999/api/reset-rocketchat

# Restart and Reset Plane to default. It may take 2~3 minutes
curl -X POST http://the-agent-company.com:2999/api/reset-plane

# Restart and Reset gitlab to default. It may take 5 minutes
curl -X POST http://the-agent-company.com:2999/api/reset-gitlab

# Reset the document data of nextcloud to default. It may take 10 seconds
curl -X POST http://the-agent-company.com:2999/api/reset-nextcloud

# health check gitlab
curl http://the-agent-company.com:2999/api/healthcheck/gitlab

# health check nextcloud
curl http://the-agent-company.com:2999/api/healthcheck/nextcloud

# health check rocketchat
curl http://the-agent-company.com:2999/api/healthcheck/rocketchat

# health check plane
curl http://the-agent-company.com:2999/api/healthcheck/plane

```
