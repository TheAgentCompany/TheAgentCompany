import requests
import logging
import os
import sys
import subprocess

from typing import List

from scoring import Result, Checkpoint
from common import *

def grade_checkpoint1():
    try:
        result = subprocess.run(['git', '-C', '/workspace/sotopia', 'branch', '--list', 'feature/dev-container'], capture_output=True, text=True)
        if 'feature/dev-container' in result.stdout:
            logging.info("Branch 'feature/dev-container' exists in the local repository.")
            return True
        else:
            logging.warning("Branch 'feature/dev-container' does not exist in the local repository.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the local repository: {e}")
        return False

def grade_checkpoint2():
    try:
        devcontainer_path = '/workspace/sotopia/.devcontainer/devcontainer.json'
        if os.path.exists(devcontainer_path):
            logging.info(".devcontainer folder and devcontainer.json file created successfully.")
            return True
        else:
            logging.warning(".devcontainer folder or devcontainer.json file not found.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the .devcontainer folder: {e}")
        return False

def grade_checkpoint3():
    try:
        # Check for Redis and Ollama support setup
        with open('/workspace/sotopia/.devcontainer/devcontainer.json', 'r') as file:
            content = file.read()
        predicate = "Redis and Ollama support set up successfully. An successful example would be something like `\"features\": { \"ghcr.io/itsmechlark/features/redis-server:1\": {}, \"ghcr.io/prulloac/devcontainer-features/ollama:1\": {} }`"
        llm_result = evaluate_with_llm(content, predicate)
        if llm_result:
            logging.info("Redis and Ollama support set up successfully.")
            return True
        else:
            logging.warning("Redis or Ollama support not set up.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking Redis and Ollama support: {e}")
        return False

def grade_checkpoint4():
    try:
        # Check for poetry, sotopia, and Llama 3.2 1b setup using LLM
        with open('/workspace/sotopia/.devcontainer/devcontainer.json', 'r') as file:
            content = file.read()
        predicate = 'Poetry and sotopia installed, and Llama 3.2 1b serving on start. A successful example would be "postCreateCommand": "pipx install poetry; poetry install --all-extras; ollama pull llama3.2:1b" in the devcontainer.json file.'
        llm_result = evaluate_with_llm(content, predicate)
        if llm_result:
            logging.info("Poetry and sotopia installed, and Llama 3.2 1b serving on start.")
            return True
        else:
            logging.warning("Poetry or sotopia not installed, or Llama 3.2 1b not serving on start.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking poetry, sotopia installation, or Llama serving: {e}")
        return False

def grade_checkpoint5():
    try:
        response = make_gitlab_request(project_identifier="root/sotopia", additional_path="merge_requests?state=opened")
        if response is not None and response.status_code == 200:
            logging.info(f"Found {len(response.json())} open merge requests")
            for i in response.json():
                if i['source_branch'] == 'feature/dev-container':
                    return True
            return False
        else:
            logging.warning(f"Unexpected status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: Clone the repository
    passed_checkpoint1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint1)))

    # Checkpoint 2: Create .devcontainer folder and devcontainer.json file
    passed_checkpoint2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint2)))

    # Checkpoint 3: Set up Redis and Ollama support
    passed_checkpoint3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed_checkpoint3)))

    # Checkpoint 4: Install poetry and sotopia, and serve Llama 3.2 1b on start
    passed_checkpoint4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(2, 2 * int(passed_checkpoint4)))

    # Checkpoint 5: Make a pull request
    passed_checkpoint5 = grade_checkpoint5()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint5)))

    return result



