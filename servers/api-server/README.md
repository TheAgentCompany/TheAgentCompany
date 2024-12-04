# API SERVER

Remember to do `/etc/host` change as mentioned [here](../README.md). Alternatively, you need to replace the following
`the-agent-company.com` with real hostname where your services are served.

```bash
# Reset the data of RocketChat to default. It may take ~1 minutes
curl -X POST http://the-agent-company.com:2999/api/reset-rocketchat

# Restart and Reset Plane to default. It may take 2~3 minutes
curl -X POST http://the-agent-company.com:2999/api/reset-plane

# Restart and Reset gitlab to default. It may take 5 minutes
curl -X POST http://the-agent-company.com:2999/api/reset-gitlab

# Restart and Reset ownCloud to default. It may take ~1 minute
curl -X POST http://the-agent-company.com:2999/api/reset-owncloud

# health check gitlab
curl http://the-agent-company.com:2999/api/healthcheck/gitlab

# health check owncloud
curl http://the-agent-company.com:2999/api/healthcheck/owncloud

# health check rocketchat
curl http://the-agent-company.com:2999/api/healthcheck/rocketchat

# health check plane
curl http://the-agent-company.com:2999/api/healthcheck/plane
```
