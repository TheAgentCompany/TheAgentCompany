import os
import logging

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm
from common import create_rocketchat_client, grader, get_rocketchat_personal_chat_history

# Create RocketChat instance
rocket = create_rocketchat_client()

def check_final_result(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return False

    # Read the content of the file and call litellm
    content = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if len(content) == 0:
        logging.warning("there is no content in the txt")
        return False

    predicate = 'No meeting scheduled this week'
    return evaluate_with_llm(content, predicate)


@grader
def grade_checkpoint1(username='Emily Zhou'):
    msgs = get_rocketchat_personal_chat_history(rocket, username)
    return len(msgs)>0

@grader
def grade_checkpoint2(username='Liu Qiang'):
    msgs = get_rocketchat_personal_chat_history(rocket, username)
    return len(msgs)>0

@grader
def grade_checkpoint3(file_path = '/workspace/conclusion.txt'):
    return check_final_result(file_path=file_path)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 2,
        grade_checkpoint3: 3
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result



