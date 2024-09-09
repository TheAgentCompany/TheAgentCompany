import json
import os
import subprocess


# Load the JSON file
with open('scenarios.json', 'r') as file:
    data = json.load(file)

# Extract keys (names) into a list
names = list(data.keys())

# Loop through the names and execute the command
for name in names:
    print(f"Launching {name}")
    command = f"python run_one_npc.py --agent_first_name={name}"
    subprocess.Popen(command, shell=True)

# Use following code to kill the backgroup npc
# pkill -f 'python run_one_npc.py'
# ps aux | grep 'python run_one_npc.py'