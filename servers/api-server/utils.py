from rocketchat_API.rocketchat import RocketChat
import redis
from redis_om import JsonModel
from redis_om.model.model import Field
import subprocess
import os
import threading
import requests
import time
import json
import logging


SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'localhost'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
PLANE_PORT = os.getenv('PLANE_PORT') or '8091'
PLANE_BASEURL = f"http://{SERVER_HOSTNAME}:{PLANE_PORT}"
PLANE_WORKSPACE_SLUG = os.getenv("PLANE_WORKSPACE_SLUG") or "tac"
PLANE_API_KEY = os.environ.get("PLANE_API_KEY") or "plane_api_83f868352c6f490aba59b869ffdae1cf"
PLANE_HEADERS = {
    "x-api-key": PLANE_API_KEY,
    "Content-Type": "application/json"
}
agent_definitions = []
with open('/rocketchat/npc_definition.json', 'r') as file:
    agent_definitions = json.load(file)
    print(f"NPC definitions loaded, number of NPCs = {len(agent_definitions)}")
HOSTNAME = os.getenv('HOSTNAME', "localhost")
EXECUTION_DIR = os.getenv('EXECUTION_DIR', "/workspace")
SKIP_SETUP = os.getenv('SKIP_SETUP', 'False').lower() == 'true'

def login_to_plane():
    res = []
    try:
        res = get_all_plane_projects()
        if len(res) == 0:
            return 400, "failed to login"
        else:
            return 200, "login success"
    except Exception as e:
        print(f"{e}")
        return 400, "failed to login"

def get_all_plane_projects():
    """Get all projects in plane."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print(f"Get all projects failed: {e}")
        return []

def create_rocketchat_client(username='theagentcompany', password='theagentcompany'):
    SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'localhost'
    ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
    
    # Construct RocketChat URL
    ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
    
    try:
        return RocketChat(username, password, server_url=ROCKETCHAT_URL)
    except:
        logging.warning("Fail to connect to rocketchat")
    return None

def wait_for_redis(host='localhost', port=6379, password='theagentcompany', retries=3, delay=1):
    client = redis.StrictRedis(host=host, port=port, password=password)
    
    for attempt in range(retries):
        try:
            # Test if Redis is responding to PING command
            if client.ping():
                print("Redis is up and running!")
                return True
        except redis.exceptions.ConnectionError:
            print(f"Attempt {attempt + 1} failed: Redis not available yet, retrying in {delay} seconds...")
            time.sleep(delay)
    print("Failed to connect to Redis after several retries.")
    return False

class AgentProfile(JsonModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    age: int = Field(index=True, default_factory=lambda: 0)
    occupation: str = Field(index=True, default_factory=lambda: "")
    gender: str = Field(index=True, default_factory=lambda: "")
    gender_pronoun: str = Field(index=True, default_factory=lambda: "")
    public_info: str = Field(index=True, default_factory=lambda: "")
    big_five: str = Field(index=True, default_factory=lambda: "")
    moral_values: list[str] = Field(index=False, default_factory=lambda: [])
    schwartz_personal_values: list[str] = Field(index=False, default_factory=lambda: [])
    personality_and_values: str = Field(index=True, default_factory=lambda: "")
    decision_making_style: str = Field(index=True, default_factory=lambda: "")
    secret: str = Field(default_factory=lambda: "")
    model_id: str = Field(default_factory=lambda: "")
    mbti: str = Field(default_factory=lambda: "")
    tag: str = Field(
        index=True,
        default_factory=lambda: "",
        description="The tag of the agent, used for searching, could be convenient to document agent profiles from different works and sources",
    )
    class Meta:
        global_key_prefix = ""  # clear prefix
        model_key_prefix = "sotopia.database.persistent_profile.AgentProfile"  # set correct prefix to match sotopia package

def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Web service is up!")
            return 200, "Web service is up!"
        else:
            return response.status_code, "Web service is not available yet"
    except requests.ConnectionError:
        print("Web service is not available yet. Retrying...")
        return 500, "Web service is not available yet"

def execute_command(command):
    try:
        print(EXECUTION_DIR, command)
        os.chdir(EXECUTION_DIR)
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Command execute failed: {e}"
    except Exception as e:
        return f"Error : {e}"

def async_execute_command(command):
    threading.Thread(target=execute_command, args=(command,)).start()
