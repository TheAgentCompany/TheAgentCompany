#!/bin/sh
set -ex

########## PRE INIT PHASE ############
python_default /utils/pre_init.py
######################################


########## RUN INITIALIZATION ########
# set up task-specific NPC ENV, only if NPC is required
python /npc/run_multi_npc.py
######################################


########## POST INIT PHASE ###########
python_default /utils/post_init.py
######################################
