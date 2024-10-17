#!/bin/sh
set -ex

########## PRE INIT PHASE ############
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
if [ -f "/utils/post_init.py" ]; then
    python_default /utils/post_init.py
fi
######################################