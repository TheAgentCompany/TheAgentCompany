FROM base-image

# persist utilities files in the exam image
COPY evaluator.py /utils/
COPY init.sh /utils/
RUN chmod +x /utils/init.sh

# This task needs to do some sanity checks when the container spins up
# those files are optional and benchmark developers should customize according
# to their tasks' needs
COPY pre_init.py /utils/
COPY populate_data.py /utils/
COPY post_init.py /utils/

# persist instruction files needed by the examinee
COPY task.md /instruction/

# requests library is needed for this task's evaluation
# this is optional and benchmark developers should customize according
# to their tasks' needs
RUN pip install requests
RUN pip install rocketchat_API==1.32.0

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY scenarios.json /npc