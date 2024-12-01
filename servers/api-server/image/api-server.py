from flask import Flask, jsonify
import subprocess
import os
import json
import threading
import requests
import os
import time
from rocketchat_API.rocketchat import RocketChat
import redis

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

app = Flask(__name__)

HOSTNAME= os.getenv('HOSTNAME', "localhost")

EXECUTION_DIR = os.getenv('EXECUTION_DIR', "/workspace")

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

@app.route('/api/reset-owncloud', methods=['POST'])
def reset_owncloud():
    # owncloud reset is essentially a restart
    # since it takes a while to stop, we need to make sure this is synchronous
    execute_command('make reset-owncloud')
    return jsonify({"message": "Reset ownCloud command initiated"}), 202

@app.route('/api/reset-rocketchat', methods=['POST'])
def reset_rocketchat():
    async_execute_command('make reset-sotopia-redis')
    async_execute_command('make reset-rocketchat')
    return jsonify({"message": "Reset RocketChat command initiated"}), 202

@app.route('/api/reset-plane', methods=['POST'])
def reset_plane():
    async_execute_command('make reset-plane')
    return jsonify({"message": "Reset Plane command initiated"}), 202

@app.route('/api/reset-gitlab', methods=['POST'])
def reset_gitlab():
    # gitlab reset is essentially a restart
    # since it takes a while to stop, we need to make sure this is synchronous
    # devnote: health check + polling on client side is still needed because
    # gitlab service takes a while to fully function after the container starts
    execute_command('make reset-gitlab')
    return jsonify({"message": "Reset GitLab command initiated"}), 202

@app.route('/api/healthcheck/owncloud', methods=['GET'])
def healthcheck_owncloud():
    code, msg = check_url("http://localhost:8092")
    return jsonify({"message":msg}), code

@app.route('/api/healthcheck/gitlab', methods=['GET'])
def healthcheck_gitlab():
    # TODO (yufansong): this check cannot cover all case
    code, msg = check_url("http://localhost:8929")
    return jsonify({"message":msg}), code

@app.route('/api/healthcheck/rocketchat', methods=['GET'])
def healthcheck_rocketchat():
    rocketchat_cli = create_rocketchat_client()
    rocketchat_code = 400 if rocketchat_cli is None else 200
    redis_msg, redis_code = healthcheck_redis()
    code = 200 if redis_code == 200 and rocketchat_code == 200 else 400
    return jsonify({"redis": redis_code, "rocketchat": rocketchat_code}), code

@app.route('/api/healthcheck/plane', methods=['GET'])
def healthcheck_plane():
    code, msg = login_to_plane()
    return jsonify({"message":msg}), code
    
@app.route('/api/healthcheck/redis', methods=['GET'])
def healthcheck_redis():
    success = wait_for_redis()
    if success:
        return jsonify({"message":"success connect to redis"}), 200
    else:
        return jsonify({"message":"failed connect to redis"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2999)
