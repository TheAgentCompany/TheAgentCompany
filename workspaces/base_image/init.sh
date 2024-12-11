#!/bin/sh
set -e

########## PRE INIT PHASE ############

# Use synthetic service hostname, the-agent-company.com in tasks and point it
# to the real service host
SERVICE_IP=$(ping -c 1 ${SERVER_HOSTNAME:-localhost} | grep PING | awk -F'[()]' '{print $2}')
echo "$SERVICE_IP the-agent-company.com" >> /etc/hosts

echo "Resetting services..."
bash /utils/reset.sh

if [ -f "/utils/pre_init.sh" ]; then
    bash /utils/pre_init.sh
fi

if [ -f "/utils/pre_init.py" ]; then
    python_default /utils/pre_init.py
fi
######################################

########## RUN INITIALIZATION ########
# set up task-specific NPC ENV, only if NPC is required
if [ -f "/npc/scenarios.json" ]; then
    python_default /npc/run_multi_npc.py
fi

# populate task-specific data if applicable
if [ -f "/utils/populate_data.py" ]; then
    python_default /utils/populate_data.py
fi
######################################

########## POST INIT PHASE ###########
if [ -f "/utils/post_init.sh" ]; then
    bash /utils/post_init.sh
fi

if [ -f "/utils/post_init.py" ]; then
    python_default /utils/post_init.py
fi
######################################