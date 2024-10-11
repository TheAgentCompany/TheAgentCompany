#!/bin/sh
set -ex

########## PRE INIT PHASE ############
python /utils/pre_init.py
######################################


########## POST INIT PHASE ###########
python /utils/post_init.py
######################################
