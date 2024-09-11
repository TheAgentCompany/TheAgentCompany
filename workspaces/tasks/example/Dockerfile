FROM base-image

# persist evaluator and task files in the exam image
COPY evaluator.py /evaluation/
COPY task.md /instruction/

# requests library is needed for this task's evaluation
# this is optional and benchmark developers should customize according
# to their tasks' needs
RUN pip install requests

# copy and run initialization code (optional)

COPY init.sh /
COPY init.py /

# Run init scripts (optional)
RUN chmod +x /init.sh
RUN sh /init.sh
RUN python /init.py

############## TEMPLATE 1: NPC is required ###################
# Set up task-specific NPC ENV
COPY scenarios.json /npc

# Set up NPC environment and keep the container running (optional)
CMD python /npc/run_multi_npc.py && tail -f /dev/null
##############################################################


############## TEMPLATE 2: NPC not needed  ###################
# Keep the container running (optional)
# CMD ["tail", "-f","/dev/null"]
##############################################################