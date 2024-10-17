FROM base-image

# Install Python requests library
RUN pip install sotopia==0.1.0-rc.1

COPY *.py /workspace
COPY *.json /workspace

# Redis Username: default, Password: jobbench
# Redis service URL: URL/:6379
ENV REDIS_OM_URL redis://default:jobbench@redis-stack:6379
# RocketChat NPC name, password, RocketChat service URL
# keep the container running (optional)
CMD python populate_data.py