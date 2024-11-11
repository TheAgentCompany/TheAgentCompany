import logging
import os
import subprocess
from sotopia.database import AgentProfile

from typing import List

from scoring import Result, Checkpoint
from common import *

@grader
def grade_checkpoint1():
    try:
        result = subprocess.run(['git', '-C', '/workspace/sotopia', 'branch', '--list', 'feature/add-new-characters'], capture_output=True, text=True)
        if 'feature/add-new-characters' in result.stdout:
            logging.info("Branch 'feature/add-new-characters' exists in the local repository.")
            return True
        else:
            logging.warning("Branch 'feature/add-new-characters' does not exist in the local repository.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the local repository: {e}")
        return False

@grader
def grade_checkpoint2():
    try:
        if os.path.exists('/workspace/sotopia/data/medical_characters.jsonl'):
            logging.info("File 'medical_characters.jsonl' found in the data folder.")
            return True
        else:
            logging.warning("File 'medical_characters.jsonl' not found in the data folder.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the data folder: {e}")
        return False

@grader
def grade_checkpoint3():
    try:
        import json

        file_path = '/workspace/sotopia/data/medical_characters.jsonl'
        if not os.path.exists(file_path):
            logging.warning("File 'medical_characters.jsonl' not found in the data folder.")
            return False

        doctors = {'male': 0, 'female': 0}
        nurses = {'male': 0, 'female': 0}

        with open(file_path, 'r') as file:
            for line in file:
                character = json.loads(line)
                try:
                    AgentProfile.parse_obj(character)
                except Exception as e:
                    logging.error(f"Error occurred while loading the character: {e}")
                    return False
                if character['occupation'].lower() == 'doctor':
                    if character['gender'].lower() == 'male':
                        doctors['male'] += 1
                    elif character['gender'].lower() == 'female':
                        doctors['female'] += 1
                elif character['occupation'].lower() == 'nurse':
                    if character['gender'].lower() == 'male':
                        nurses['male'] += 1
                    elif character['gender'].lower() == 'female':
                        nurses['female'] += 1

        if doctors['male'] == 3 and doctors['female'] == 3 and nurses['male'] == 3 and nurses['female'] == 3:
            logging.info("The 'medical_characters.jsonl' file has the correct number of doctors and nurses with balanced genders.")
            return True
        else:
            logging.warning("The 'medical_characters.jsonl' file does not have the correct number of doctors and nurses with balanced genders.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the 'medical_characters.jsonl' file: {e}")
        return False
    

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: create branch
    passed_checkpoint1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint1)))

    # Checkpoint 2: medical_characters.jsonl is present
    passed_checkpoint2 = passed_checkpoint1 and grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint2)))

    # Checkpoint 3: Gender parity check passed
    passed_checkpoint3 = passed_checkpoint2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed_checkpoint3)))

    return result



