#!/bin/sh
set -ex

########## PRE INIT PHASE ############
python_default /utils/pre_init.py
######################################

########## RUN INITIALIZATION ########
######################################

########## POST INIT PHASE ###########
python_default /utils/post_init.py
######################################
