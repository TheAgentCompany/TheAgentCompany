import requests
import logging
import os
import sys
from rocketchat_API.rocketchat import RocketChat # type: ignore
import subprocess
import json
from typing import List

from scoring import Result, Checkpoint
from common import *

def grade_checkpoint1():
    try:
        result = subprocess.run(['git', '-C', '/workspace/sotopia', 'branch', '--list', 'feature/nonVerbalAgent'], capture_output=True, text=True)
        if 'feature/nonVerbalAgent' in result.stdout:
            logging.info("Branch 'feature/nonVerbalAgent' exists in the local repository.")
            return True
        else:
            logging.warning("Branch 'feature/nonVerbalAgent' does not exist in the local repository.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the local repository: {e}")
        return False

def grade_checkpoint2():
    try:
        with open('/workspace/sotopia/sotopia/agents/llm_agent.py', 'r') as file:
            content = file.read()
            if 'class NonVerbalAgent' in content:
                logging.info("Class 'NonVerbalAgent' found in llm_agent.py.")
                if 'class NonVerbalAgent(LLMAgent)' in content:
                    logging.info("Class 'NonVerbalAgent' inherits from 'LLMAgent'.")
                    return True
                else:
                    logging.warning("Class 'NonVerbalAgent' does not inherit from 'LLMAgent'.")
                    return False
            else:
                logging.warning("Class 'NonVerbalAgent' not found in llm_agent.py.")
                return False
    except FileNotFoundError:
        logging.error("File llm_agent.py not found.")
        return False
    except Exception as e:
        logging.error(f"Error occurred while checking llm_agent.py: {e}")
        return False

def grade_checkpoint3():
    try:
        response = make_gitlab_request(project_identifier="root/sotopia", additional_path="merge_requests?state=opened")
        if response is not None and response.status_code==200:
            logging.info(f"Found {len(response.json())} open merge requests")
            for i in response.json():
                if i['source_branch'] == 'feature/nonVerbalAgent':
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

    # Checkpoint 1: create branch
    passed_checkpoint1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint1)))

    # Checkpoint 2: NonVerbalAgent class implemented
    passed_checkpoint2 = passed_checkpoint1 and grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint2)))

    # Checkpoint 3: Merge request created
    passed_checkpoint3 = passed_checkpoint2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(3, 3 * int(passed_checkpoint3)))

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
