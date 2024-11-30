from flask import Flask, jsonify
import subprocess
import os
import json
import threading
import requests
import os

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'localhost'
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

app = Flask(__name__)

HOSTNAME= os.getenv('HOSTNAME', "localhost")

EXECUTION_DIR = os.getenv('EXECUTION_DIR', "workspace")

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
    rocketchat_code, rocketchat_msg = check_url("http://localhost:3000")
    redis_code, redis_msg = check_url("http://localhost:6379")
    message = {
        "rocketchat_msg": rocketchat_msg,
        "redis_msg": redis_msg,
    }
    # redis check not work, has bug, temporarily disable it
    # code = 200 if redis_code == 200 and rocketchat_code == 200 else 500
    code = rocketchat_code

    return jsonify({"message": message, "redis": redis_code == 200, "rocketchat": rocketchat_code == 200}), code

@app.route('/api/healthcheck/plane', methods=['GET'])
def healthcheck_plane():
    code, msg = login_to_plane()
    return jsonify({"message":msg}), code
    

# Not work, has bug
@app.route('/api/healthcheck/redis', methods=['GET'])
def healthcheck_redis():
    code, msg = check_url("http://localhost:6379")
    return jsonify({"message":msg}), code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2999)
