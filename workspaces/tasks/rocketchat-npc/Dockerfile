FROM base-image

# Install Python requests library
RUN pip install rocketchat_API==1.32.0
RUN pip install sotopia==0.1.0-rc.1

# create npc directory (examinee MUST not access this directory)
RUN mkdir -p /npc

COPY *.json  /npc
COPY *.py /npc

# Redis Username: default, Password: jobbench
# Redis service URL: ogma.lti.cs.cmu.edu/:6379
ENV REDIS_OM_URL redis://default:jobbench@ogma.lti.cs.cmu.edu/:6379
# RocketChat service URL
ENV BOT_URL http://ogma.lti.cs.cmu.edu:3000
ENV CREDENTIAL_FILE_PATH /npc/npc_credential.json
ENV SCENARIOS_FILE_PATH /npc/scenarios.json
# If you want to launch the rocketchat npc, you need to do the following thing in your examinee

# Step1: set OPENAI API KEY
# ENV OPENAI_API_KEY <Your OPENAI_API_KEY>

# Step2: COPY scenarios.json to docker with your own definition

# Step3: execute the run_multi_npc.py in npc directory.
# CMD python /npc/run_multi_npc.py