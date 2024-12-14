FROM ghcr.io/theagentcompany/task-base-image:1.0.0

COPY populate_data.py /workspace
COPY evaluator.py /utils
COPY *.json /workspace

# Redis Username: default, Password: theagentcompany
# Redis service URL: URL/:6379
ENV REDIS_OM_URL redis://default:theagentcompany@redis-stack:6379
# RocketChat NPC name, password, RocketChat service URL
# keep the container running (optional)
CMD python populate_data.py