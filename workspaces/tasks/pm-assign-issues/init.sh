#!/bin/sh
set -ex

########## PRE INIT PHASE ############
python_default /utils/pre_init.py
######################################

########## RUN INITIALIZATION ########
python_default /utils/populate_data.py
######################################