#!/bin/sh
# You should do the initialization work in this script to set up the environment you need

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi



################### Example about Launch NPC ############################
############### Please delete it if you don't need ######################


BLOCKED_DOMAINS=${BLOCKED_DOMAINS:-"youtube.com reddit.com"}

python /npc/run_multi_npc.py
echo "Hosts file updated successfully"