import json
import time
import os
import subprocess


scenarios_file_path = os.getenv('SCENARIOS_FILE_PATH') or 'scenarios.json'
openai_api_key = os.getenv('OPENAI_API_KEY')
LITELLM_API_KEY = os.getenv('LITELLM_API_KEY')
LITELLM_BASE_URL = os.getenv('LITELLM_BASE_URL')
LITELLM_MODEL = os.getenv('LITELLM_MODEL')

# Load the JSON file
with open(scenarios_file_path, 'r') as file:
    data = json.load(file)

# Extract keys (names) into a list
names = list(data.keys())

# Loop through the names and execute the command
for name in names:
    print(f"Launching {name}")
    command = f"LITELLM_API_KEY={LITELLM_API_KEY} LITELLM_BASE_URL={LITELLM_BASE_URL} LITELLM_MODEL={LITELLM_MODEL} python_default /npc/run_one_npc.py --agent_name=\"{name}\""
    print(command)
    # do not let it print logs to stdout
    subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# sleep 30 seconds so that NPC processes are launched
time.sleep(30)

# Use following code to kill the backgroup npc
# pkill -f 'python run_one_npc.py'
# ps aux | grep 'python run_one_npc.py'