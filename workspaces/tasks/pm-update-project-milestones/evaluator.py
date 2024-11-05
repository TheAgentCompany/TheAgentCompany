import logging
from datetime import datetime
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_any_of_given_checkpoints
from common import make_gitlab_request
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 1  
CHECKPOINT_2_POINTS = 1  
CHECKPOINT_3_POINTS = 1  
CHECKPOINT_4_POINTS = 1  
CHECKPOINT_5_POINTS = 1  

PROJECT_NAME = 'risingwave'
PROJECT_PATH = f"{GITLAB_USER}/{PROJECT_NAME}"
MILESTONES_URL = f"root/{PROJECT_NAME}/-/milestones"
ISSUE_1_TITLE = 'Implement stream processing engine'
ISSUE_2_TITLE = 'Integrate with Kafka'

MILESTONE_1 = 'Alpha Release'
MILESTONE_2 = 'Beta Release'

def grade_checkpoint1(trajectory):
    # Check if the agent visited the milestones page
    return MILESTONES_URL in trajectory

def grade_checkpoint2():
    # Check if "Alpha Release" milestone is closed
    response = make_gitlab_request(PROJECT_PATH, 'milestones', params={'search': MILESTONE_1})
    if response is None or response.status_code != 200:
        return False
    milestones = response.json()
    for milestone in milestones:
        if milestone['title'] == MILESTONE_1 and milestone['state'] == 'closed':
            return True
    return False

def grade_checkpoint3():
    # Check if "Beta Release" milestone is created
    response = make_gitlab_request(PROJECT_PATH, 'milestones', params={'search': MILESTONE_2})
    if response is None or response.status_code != 200:
        return False

    milestones = response.json()
    for milestone in milestones:
        if milestone['title'] == MILESTONE_2:
            return True
    return False

def grade_checkpoint4():
    # Check if "Implement stream processing engine" is assigned to "Beta Release" milestone
    response = make_gitlab_request(PROJECT_PATH, 'issues', params={'search': ISSUE_1_TITLE})
    if response is None or response.status_code != 200:
        return False
    issues = response.json()
    for issue in issues:
        if issue['title'] == ISSUE_1_TITLE:
            milestone = issue.get('milestone')
            if milestone and milestone['title'] == MILESTONE_2:
                return True
    return False

def grade_checkpoint5():
    # Check if "Integrate with Kafka" is assigned to "Beta Release" milestone
    response = make_gitlab_request(PROJECT_PATH, 'issues', params={'search': ISSUE_2_TITLE})
    if response is None or response.status_code != 200:
        return False
    issues = response.json()
    for issue in issues:
        if issue['title'] == ISSUE_2_TITLE:
            milestone = issue.get('milestone')
            if milestone and milestone['title'] == MILESTONE_2:
                return True
    return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any_of_given_checkpoints([2, 3]))

    # Checkpoint 1: Visited the milestones page
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    # Checkpoint 2: Closed the "Alpha Release" milestone
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    # Checkpoint 3: Created the "Beta Release" milestone
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed3)))

    # Checkpoint 4: Assigned "Implement stream processing engine" to "Beta Release" milestone 
    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(CHECKPOINT_4_POINTS, CHECKPOINT_4_POINTS * int(passed4)))

    # Checkpoint 5: Assigned "Integrate with Kafka" to "Beta Release" milestone
    passed5 = grade_checkpoint5()
    checkpoints.append(Checkpoint(CHECKPOINT_5_POINTS, CHECKPOINT_5_POINTS * int(passed5)))

    return result
