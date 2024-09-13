FROM base-image
################### BUILD TIME ###################
# All build time work should did by writing dockerfile

# persist evaluator and task files in the exam image
COPY evaluator.py /evaluation/
COPY task.md /instruction/
COPY init.sh /workspace
RUN chmod +x /workspace/init.sh
# Optional for benchmark developers
COPY prerequisite.py /workspace/ 

# requests library is needed for this task's evaluation
# this is optional and benchmark developers should customize according
# to their tasks' needs
RUN pip install requests

# Set up task-specific NPC ENV, and Run it in init.sh
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY scenarios.json /npc

################### RUN TIME ###################
# The benchmark task builder should put all run time work into init.sh, and NOT execute it via CMD.
# The bencgmark user should execute init.sh by themselves.
CMD sh /workspace/init.sh