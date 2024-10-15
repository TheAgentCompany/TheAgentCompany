#!/bin/sh
set -ex

########## PRE INIT PHASE ############
python_default /utils/pre_init.py
######################################

########## POST INIT PHASE ###########
python_default /utils/post_init.py
######################################
