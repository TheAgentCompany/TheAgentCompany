FROM base-image

# NPCs are needed in this task, so we need to persist "scenarios.json"
# this is optional and benchmark developers should customize according
# to their tasks' needs
COPY scenarios.json /npc

# Copy files into the workspace
COPY events-viewer.zip /workspace/
COPY events.db /workspace/
