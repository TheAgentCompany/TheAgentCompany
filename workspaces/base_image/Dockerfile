################## BASE IMAGE ######################
FROM python:3

# create evaluation directory (examinee MUST not access this directory)
RUN mkdir -p /evaluation

# create instruction directory (examinee should read instructions from here)
RUN mkdir -p /instruction
COPY test_setup.py /instruction

# create and set up working directory
RUN mkdir -p /workspace
WORKDIR /workspace

################## BASE NPC IMAGE ######################

# Install Python requests library
RUN pip install rocketchat_API==1.32.0
RUN pip install sotopia==0.1.0-rc.1

# create npc directory (examinee MUST not access this directory)
RUN mkdir -p /npc

COPY *.json  /npc
COPY *.py /npc

ENV CREDENTIAL_FILE_PATH /npc/npc_credential.json
ENV SCENARIOS_FILE_PATH /npc/scenarios.json