FROM base-image

# Install Python requests library
RUN pip install rocketchat_API==1.32.0
RUN pip install sotopia==0.1.0-rc.1

COPY *.json  /workspace
COPY *.py /workspace

# Redis Username: default, Password: jobbench
# Redis service URL: ogma.lti.cs.cmu.edu/:6379
ENV REDIS_OM_URL redis://default:jobbench@ogma.lti.cs.cmu.edu/:6379
# RocketChat service URL
ENV BOT_URL http://ogma.lti.cs.cmu.edu:3000
ENV OPENAI_API_KEY <Your OPENAI_API_KEY>
# keep the container running (optional)
CMD python main.py --agent_first_name=John