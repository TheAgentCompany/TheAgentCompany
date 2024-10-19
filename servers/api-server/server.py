from flask import Flask, jsonify
import subprocess
import os
import json
import threading

app = Flask(__name__)

EXECUTION_DIR = '/home/yufansong/JobBench/servers'

def execute_command(command):
    try:
        os.chdir(EXECUTION_DIR)
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Command execute failed: {e}"
    except Exception as e:
        return f"Error : {e}"

def async_execute_command(command):
    threading.Thread(target=execute_command, args=(command,)).start()

@app.route('/api/nextcloud-config', methods=['GET'])
def get_nextcloud_config():
    output = execute_command('docker exec nextcloud-aio-mastercontainer cat /mnt/docker-aio-config/data/configuration.json')
    try:
        config = json.loads(output)
        password = config.get('secrets', {}).get('NEXTCLOUD_PASSWORD')
        if password:
            return jsonify({"NEXTCLOUD_PASSWORD": password})
        else:
            return jsonify({"error": "NEXTCLOUD_PASSWORD not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse JSON output"}), 500

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
    async_execute_command('make reset-gitlab')
    return jsonify({"message": "Reset GitLab command initiated"}), 202

@app.route('/api/reset-nextcloud', methods=['POST'])
def reset_nextcloud():
    async_execute_command('make reset-nextcloud')
    return jsonify({"message": "Reset Nextcloud command initiated"}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2999)