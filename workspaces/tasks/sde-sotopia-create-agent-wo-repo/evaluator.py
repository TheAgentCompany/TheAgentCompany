import requests
import logging
import os
import sys
import subprocess

from typing import List

from scoring import Result, Checkpoint
from common import *

@checkpoint
def grade_checkpoint1():
    try:
        if os.path.isdir('/workspace/sotopia'):
            logging.info("Repository already cloned.")
            return True
        else:
            logging.warning("Repository not cloned.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False

@checkpoint
def grade_checkpoint2():
    try:
        result = subprocess.run(['git', '-C', '/workspace/sotopia', 'branch', '--list', 'feature/actionAgent'], capture_output=True, text=True)
        if 'feature/actionAgent' in result.stdout:
            logging.info("Branch 'feature/actionAgent' exists in the local repository.")
            return True
        else:
            logging.warning("Branch 'feature/actionAgent' does not exist in the local repository.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the local repository: {e}")
        return False

@checkpoint
def grade_checkpoint3():
    try:
        with open('/workspace/sotopia/sotopia/agents/llm_agent.py', 'r') as file:
            content = file.read()
            if 'class ActionAgent' in content:
                logging.info("Class 'ActionAgent' found in llm_agent.py.")
                if 'class ActionAgent(LLMAgent)' in content:
                    logging.info("Class 'ActionAgent' inherits from 'LLMAgent'.")
                    return True
                else:
                    logging.warning("Class 'ActionAgent' does not inherit from 'LLMAgent'.")
                    return False
            else:
                logging.warning("Class 'ActionAgent' not found in llm_agent.py.")
                return False
    except FileNotFoundError:
        logging.error("File llm_agent.py not found.")
        return False
    except Exception as e:
        logging.error(f"Error occurred while checking llm_agent.py: {e}")
        return False

@checkpoint
def grade_checkpoint4():
    try:
        # Run mypy check
        result = subprocess.run(['mypy', '/workspace/sotopia/sotopia/agents/llm_agent.py'], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Mypy check passed for llm_agent.py.")
            return True
        else:
            logging.warning(f"Mypy check failed for llm_agent.py:\n{result.stdout}\n{result.stderr}")
            return False
    except Exception as e:
        logging.error(f"Error occurred while running mypy check: {e}")
        return False


@checkpoint
def grade_checkpoint5():
    try:
        response = make_gitlab_request(project_identifier="root/sotopia", additional_path="merge_requests?state=opened")
        if response is not None and response.status_code==200:
            logging.info(f"Found {len(response.json())} open merge requests")
            for i in response.json():
                if i['source_branch'] == 'feature/actionAgent':
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

    # Checkpoint 2: create branch
    passed_checkpoint2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint2)))

    # Checkpoint 3: NonVerbalAgent class implemented
    passed_checkpoint3 = passed_checkpoint2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed_checkpoint3)))

    # Checkpoint 4: mypy check passed
    passed_checkpoint4 = passed_checkpoint3 and grade_checkpoint4()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint4)))

    # Checkpoint 5: Merge request created
    passed_checkpoint5 = passed_checkpoint4 and grade_checkpoint5()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint5)))

    return result



