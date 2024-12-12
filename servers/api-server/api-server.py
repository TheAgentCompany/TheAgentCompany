from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

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
    code, msg = check_url("http://localhost:8929")
    return jsonify({"message":msg}), code

@app.route('/api/healthcheck/rocketchat', methods=['GET'])
def healthcheck_rocketchat():
    rocketchat_cli = create_rocketchat_client()
    rocketchat_code = 400 if rocketchat_cli is None else 200
    _, redis_code = healthcheck_redis()
    # Sotopia is optional if no NPC is needed for the task,
    # but for simplicity, we always check Sotopia NPC profiles are correctly
    # loaded whenever RocketChat service is needed
    _, sotopia_code = healthcheck_sotopia()
    code = 200 if redis_code == 200 and rocketchat_code == 200 and sotopia_code == 200 else 400
    return jsonify({"redis": redis_code, "rocketchat": rocketchat_code, "sotopia": sotopia_code}), code

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

def get_by_name(first_name, last_name):
    return AgentProfile.find(
        (AgentProfile.first_name == first_name) & 
        (AgentProfile.last_name == last_name)
    ).all()

@app.route('/api/healthcheck/sotopia', methods=['GET'])
def healthcheck_sotopia():
    success = wait_for_redis()
    assert len(agent_definitions) > 0
    if success:
        for definition in agent_definitions:
            if not AgentProfile.find((AgentProfile.first_name == definition["first_name"]) & (AgentProfile.last_name == definition["last_name"])).all():
                success = False
                print(f"NPC ({definition['first_name']} {definition['last_name']}) not found")
                break
        
    if success:
        return jsonify({"message":"sotopia npc profiles loaded successfully"}), 200
    else:
        return jsonify({"message":"sotopia npc profiles not loaded"}), 400

if __name__ == '__main__':
    if SKIP_SETUP:
        print(f"Skip the setup")
    else:
        execute_command("make start-all")
    app.run(host='0.0.0.0', port=2999)
