FROM base-image

# Install Python requests library
RUN pip install rocketchat_API==1.32.0
RUN pip install sotopia==0.1.0-rc.1

COPY *.json  /workspace
COPY *.py /workspace

# Docker bridge network: 172.17.0.1, which means host machine
# Redis Username: default, Password: jobbench
# Redis service URL: 172.17.0.1:8092 
ENV REDIS_OM_URL redis://default:jobbench@172.17.0.1:8092
# RocketChat NPC name, password, RocketChat service URL
ENV BOT_NAME rocket.cat
ENV BOT_PASSWORD jobbench
ENV BOT_URL http://localhost:3000
# ENV OPENAI_API_KEY <Your OPENAI_API_KEY>

# keep the container running (optional)
CMD python main.py