################### RUN TIME ###################
############## TEMPLATE 1: NPC is required ###################
# Set up task-specific NPC ENV
python /npc/run_multi_npc.py && tail -f /dev/null
##############################################################


############## TEMPLATE 2: NPC not needed  ###################
# Keep the container running (optional)
tail -f /dev/null
##############################################################