#!/bin/sh
set -ex

########## PRE INIT PHASE ############
python_default /utils/pre_init.py
######################################

########## RUN INITIALIZATION ########
python_default /npc/run_multi_npc.py
######################################

########## POST INIT PHASE ###########
python_default /utils/post_init.py
######################################