# API SEVER

```bash
# Get nextcloud login password
curl http://ogma.lti.cs.cmu.edu:2999/api/nextcloud-config

# Reset the data of RocketChat to default. It may take ~1 minutes
curl -X POST http://ogma.lti.cs.cmu.edu:2999/api/reset-rocketchat

# Restart and Reset Plane to default. It may take 2~3 minutes
curl -X POST http://ogma.lti.cs.cmu.edu:2999/api/reset-plane

# Restart and Reset gitlab to default. It may take 5 minutes
curl -X POST http://ogma.lti.cs.cmu.edu:2999/api/reset-gitlab

# Reset the document data of nextcloud to default. It may take 10 seconds
curl -X POST http://ogma.lti.cs.cmu.edu:2999/api/reset-nextcloud

# health check gitlab
curl http://ogma.lti.cs.cmu.edu:2999/api/healthcheck/gitlab

# health check nextcloud
curl http://ogma.lti.cs.cmu.edu:2999/api/healthcheck/nextcloud

# health check rocketchat
curl http://ogma.lti.cs.cmu.edu:2999/api/healthcheck/rocketchat

# health check plane
curl http://ogma.lti.cs.cmu.edu:2999/api/healthcheck/plane

```
