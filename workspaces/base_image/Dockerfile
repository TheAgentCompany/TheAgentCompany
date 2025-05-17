FROM python:3.12

RUN apt-get update && apt-get install -y iputils-ping vim

################## Basic SETUP ################################
# create utils directory (examinee MUST not access this directory)
RUN mkdir -p /utils
COPY init.sh /utils/
RUN chmod +x /utils/init.sh
COPY reset.sh /utils/
RUN chmod +x /utils/reset.sh
COPY common.py /utils
COPY config.py /utils
COPY scoring.py /utils
COPY eval.py /utils
COPY encrypt.py /utils

# create instruction directory (examinee should read instructions from here)
RUN mkdir -p /instruction

# create and set up working directory (for examinee to complete its task)
RUN mkdir -p /workspace
WORKDIR /workspace

# create a softlink in case "python" alias is polluted
RUN ln -s /usr/local/bin/python3 /usr/local/bin/python_default

# install commonly used libraries
RUN pip install requests==2.32.3
RUN pip install cryptography==44.0.0

#############################################################

RUN apt-get install libgl1-mesa-glx -y

RUN bash -c "git clone https://github.com/li-boxuan/owl.git && cd owl && python -m venv owl_env && source owl_env/bin/activate && python -m pip install -r requirements.txt && playwright install && playwright install-deps"

################## OWL SETUP ################################

#############################################################

################## NPC SETUP ################################
# For simplicity, we set up necessary environments needed
# by NPCs in the base image, even though some simple tasks
# don't require NPCs

# Install Python libraries needed to launch NPCs
RUN pip install rocketchat_API==1.32.0
RUN pip install sotopia==0.1.2
# sotopia requires a specific hiredis version
RUN pip install hiredis==3.0.0
RUN pip install litellm==1.23.16

# create npc directory
RUN mkdir -p /npc
COPY ./npc  /npc

ENV CREDENTIAL_FILE_PATH /npc/npc_credential.json
ENV SCENARIOS_FILE_PATH /npc/scenarios.json

################## rocketchat NPC sotopia SETUP ######################
ENV REDIS_OM_URL redis://default:theagentcompany@the-agent-company.com/:6379
ENV BOT_URL http://the-agent-company.com:3000
#############################################################

################## LLM Evaluator/rocketchat NPC SETUP ###############
# If the task needs to use LLM-based evaluator OR involves NPCs, then
# LITELLM_API_KEY must be set, along with optional LITELLM_BASE_URL
# and LITELLM_MODEL variables
# ENV LITELLM_API_KEY
# ENV LITELLM_BASE_URL
# ENV LITELLM_MODEL
ENV PYTHONPATH="/utils:$PYTHONPATH"
#############################################################

################## ONBUILD (child images) SETUP #############
# persist utilities files in the exam image
ONBUILD COPY *.py /utils/

ONBUILD COPY dependencies.yml /utils/

# persist instruction files needed by the examinee
ONBUILD COPY task.md /instruction/

# prevent examinee from accessing evaluator
ONBUILD RUN python /utils/encrypt.py && rm /utils/evaluator.py /utils/encrypt.py
#############################################################
