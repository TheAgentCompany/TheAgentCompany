from flask import Flask, jsonify
import subprocess
import os
import json
import threading
import requests


app = Flask(__name__)

HOSTNAME= os.getenv('HOSTNAME', "ogma.lti.cs.cmu.edu")

# TODO (yufansong): using git to find root is hacky and wrong
def get_git_root():
    try:
        git_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=os.getcwd(),
            stderr=subprocess.STDOUT,
            universal_newlines=True
        ).strip()
        return git_root
    except subprocess.CalledProcessError:
        return None

EXECUTION_DIR = get_git_root() + '/servers'

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

@app.route('/api/reset-rocketchat', methods=['POST'])
def reset_rocketchat():
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

@app.route('/api/healthcheck/gitlab', methods=['GET'])
def healthcheck_gitlab():
    # TODO (yufansong): this check cannot cover all case
    code, msg = check_url("http://localhost:8929")
    return jsonify({"message":msg}), code

@app.route('/api/healthcheck/rocketchat', methods=['GET'])
def healthcheck_rocketchat():
    code, msg = check_url("http://localhost:3000")
    return jsonify({"message":msg}), code

@app.route('/api/healthcheck/plane', methods=['GET'])
def healthcheck_plane():
    code, msg = check_url("http://localhost:8091")
    return jsonify({"message":msg}), code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2999)
