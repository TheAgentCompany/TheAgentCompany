import os
import logging

from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, grader, evaluate_chat_history_with_llm

# Create RocketChat instance
rocket = create_rocketchat_client()
predicate = 'there is a plan to hold a kickoff meeting for the main Q4 project'

@grader
def grade_checkpoint1(username='Jessica Lee'):
    return evaluate_chat_history_with_llm(rocket, username, predicate)

@grader
def grade_checkpoint2(username='David Wong'):
    return evaluate_chat_history_with_llm(rocket, username, predicate)

@grader
def grade_checkpoint3(username='Huang Jie'):
    return evaluate_chat_history_with_llm(rocket, username, predicate)

@grader
def grade_checkpoint4(username='Mark Johnson'):
    return evaluate_chat_history_with_llm(rocket, username, predicate)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 1,
        grade_checkpoint4: 1,

    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result




