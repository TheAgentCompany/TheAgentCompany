import logging
import requests
import urllib.parse
import base64
from typing import List
import json
import os
import re

from scoring import Result, Checkpoint
from common import *



# Check if OpenHands repo is cloned
def grade_checkpoint1():
    openhands_path = '/workspace/openhands'
    try:
        # Check if the directory exists
        if not os.path.isdir(openhands_path):
            logging.warning("No dir found")
            return False
        # Get all files in the directory
        files = os.listdir(openhands_path)
        # Check if there's at least one file
        if not files:
            logging.warning("No file found")
            return False
        instruction_file_name = ".openhands_instructions"
        instruction_file_path = os.path.join(openhands_path, instruction_file_name)

        return os.path.isfile(instruction_file_path)

    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False
    
def grade_checkpoint2():
    openhands_path = '/workspace/openhands/agenthub/codeact_agent/__init__.py'
    target_str = '"CodeActAgent"'
    try:
        # Check if the directory exists
        if not os.path.exists(openhands_path):
            logging.warning("No file found")
            return False
        # Get all files in the directory
        # Check if there's at least one file
        with open(openhands_path, 'r') as file:
            file_contents = file.read()
        if target_str in file_contents:
            return True
        else:
            return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False

# Check if all unit tests pass
def grade_checkpoint3():
    openhands_path = '/workspace/openhands/agenthub/browsing_agent/__init__.py'
    target_str = '"BrowsingAgent"'
    try:
        # Check if the directory exists
        if not os.path.exists(openhands_path):
            logging.warning("No file found")
            return False
        # Get all files in the directory
        # Check if there's at least one file
        with open(openhands_path, 'r') as file:
            file_contents = file.read()
        if target_str in file_contents:
            return True
        else:
            return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False

# Check if all unit tests pass
def grade_checkpoint4():
    openhands_path = '/workspace/openhands/agenthub/__init__.py'
    target_str = '"codeact_agent"'
    try:
        # Check if the directory exists
        if not os.path.exists(openhands_path):
            logging.warning("No file found")
            return False
        # Get all files in the directory
        # Check if there's at least one file
        with open(openhands_path, 'r') as file:
            file_contents = file.read()
        if target_str in file_contents:
            return True
        else:
            return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint4: {e}")
        return False
    
def grade_checkpoint5(trajectory):
    try:
        if 'failed' in trajectory.lower():
            return False
        
        collected_match = re.search(r'collected (\d+) item(s)?', trajectory)
        if not collected_match or int(collected_match.group(1)) == 0:
            return False
        
        passed_match = re.search(r'(\d+) passed', trajectory)
        if passed_match and collected_match:
            passed_tests = int(passed_match.group(1))
            total_tests = int(collected_match.group(1))
            return passed_tests == total_tests
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint4: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    passed4 = grade_checkpoint4(trajectory)
    checkpoints.append(Checkpoint(1, int(passed4)))

    passed5 = grade_checkpoint5()
    checkpoints.append(Checkpoint(1, int(passed5)))

    return Result(checkpoints)
