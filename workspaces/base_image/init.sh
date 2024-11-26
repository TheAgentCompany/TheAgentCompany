#!/bin/sh
set -e

########## PRE INIT PHASE ############

# Use synthetic service hostname, the-agent-company.com in tasks and point it
# to the real service host
# TODO: remove ogma and use localhost before release
# we use ogma for now to make development easier
SERVICE_IP=$(ping -c 1 ${SERVER_HOSTNAME:-ogma.lti.cs.cmu.edu} | grep PING | awk -F'[()]' '{print $2}')
echo "$SERVICE_IP the-agent-company.com" >> /etc/hosts

# Reset services if declared as a dependency
# TODO: always reset once ready for release
# For now, only reset if RESET_ENV is set, so that the server doesn't suffer from
# concurrent reset calls from multiple developers
if [ -n "$RESET_ENV" ]; then
    echo "Resetting services..."
    bash /utils/reset.sh
else
    echo "Skipping service reset"
fi


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
# TODO: revisit this: do tasks really need private data?
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