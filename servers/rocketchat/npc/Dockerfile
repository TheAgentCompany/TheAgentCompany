FROM base-image

# Install Python requests library
RUN pip install sotopia==0.1.0-rc.1

COPY *.py /workspace

# Redis Username: default, Password: jobbench
# Redis service URL: ogma.lti.cs.cmu.edu/:6379
ENV REDIS_OM_URL redis://default:jobbench@ogma.lti.cs.cmu.edu/:6379
# RocketChat NPC name, password, RocketChat service URL
# keep the container running (optional)
CMD python populate_data.py