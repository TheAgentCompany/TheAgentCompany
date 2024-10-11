#!/bin/sh
set -ex

########## PRE INIT PHASE ############
python /utils/pre_init.py
######################################


########## RUN INITIALIZATION ########
# set up task-specific NPC ENV, only if NPC is required
python /npc/run_multi_npc.py
######################################


########## POST INIT PHASE ###########
python /utils/post_init.py
######################################
