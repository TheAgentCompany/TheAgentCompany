import logging
from datetime import datetime
from typing import List

from scoring import Result, Checkpoint
from common import make_gitlab_request
from config import GITLAB_USER

CHECKPOINT_1_POINTS = 1  # Visited milestones page
CHECKPOINT_2_POINTS = 1  # Closed "Alpha Release" milestone
CHECKPOINT_3_POINTS = 2  # Created "Beta Release" milestone with due date
CHECKPOINT_4_POINTS = 1  # Visited "Implement stream processing engine" issue
CHECKPOINT_5_POINTS = 1  # Visited "Integrate with Kafka" issue
CHECKPOINT_6_POINTS = 1  # Assigned "Implement stream processing engine" issue to "Beta Release" milestone
CHECKPOINT_7_POINTS = 1  # Assigned "Integrate with Kafka" issue to "Beta Release" milestone

PROJECT_NAME = 'risingwave'
PROJECT_PATH = f"{GITLAB_USER}/{PROJECT_NAME}"
BASE_URL = "http://the-agent-company.com:8929"
MILESTONES_URL = f"{BASE_URL}/root/{PROJECT_NAME}/-/milestones"
ISSUES_URL = f"{BASE_URL}/root/{PROJECT_NAME}/-/issues"
ISSUE_1_TITLE = 'Implement stream processing engine'
ISSUE_2_TITLE = 'Integrate with Kafka'

MILESTONE_1 = 'Alpha Release'
MILESTONE_2 = 'Beta Release'

# Variables to store issue URLs
ISSUE_1_URL = None
ISSUE_2_URL = None

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
    # Check if "Beta Release" milestone is created with due date on the 15th of next month
    response = make_gitlab_request(PROJECT_PATH, 'milestones', params={'search': MILESTONE_2})
    if response is None or response.status_code != 200:
        return False

    milestones = response.json()
    for milestone in milestones:
        if milestone['title'] == MILESTONE_2:
            due_date_str = milestone.get('due_date')
            if not due_date_str:
                return False
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            # Calculate expected due date (15th of next month)
            today = datetime.utcnow()
            month = today.month + 1 if today.month < 12 else 1
            year = today.year if today.month < 12 else today.year + 1
            expected_due_date = datetime(year, month, 15)
            # Allow a one-day margin for time zone differences
            if abs((due_date - expected_due_date).days) <= 1:
                return True
    return False

def get_issue_url(issue_title):
    # Get the issue URL from GitLab
    response = make_gitlab_request(PROJECT_PATH, 'issues', params={'search': issue_title})
    if response is None or response.status_code != 200:
        return None
    issues = response.json()
    for issue in issues:
        if issue['title'] == issue_title:
            return issue['web_url']
    return None

def grade_checkpoint4(trajectory):
    # Check if the agent visited the "Implement stream processing engine" issue page
    global ISSUE_1_URL
    if ISSUE_1_URL is None:
        ISSUE_1_URL = get_issue_url(ISSUE_1_TITLE)
    if ISSUE_1_URL is None:
        return False
    return ISSUE_1_URL in trajectory

def grade_checkpoint5(trajectory):
    # Check if the agent visited the "Integrate with Kafka" issue page
    global ISSUE_2_URL
    if ISSUE_2_URL is None:
        ISSUE_2_URL = get_issue_url(ISSUE_2_TITLE)
    if ISSUE_2_URL is None:
        return False
    return ISSUE_2_URL in trajectory

def grade_checkpoint6():
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

def grade_checkpoint7():
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
    result = Result(checkpoints)

    # Checkpoint 1: Visited the milestones page
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    # Checkpoint 2: Closed the "Alpha Release" milestone
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    # Checkpoint 3: Created the "Beta Release" milestone with correct due date
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed3)))

    # Checkpoint 4: Visited the "Implement stream processing engine" issue
    passed4 = grade_checkpoint4(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_4_POINTS, CHECKPOINT_4_POINTS * int(passed4)))

    # Checkpoint 5: Visited the "Integrate with Kafka" issue
    passed5 = grade_checkpoint5(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_5_POINTS, CHECKPOINT_5_POINTS * int(passed5)))

    # Checkpoint 6: Assigned "Implement stream processing engine" to "Beta Release"
    passed6 = grade_checkpoint6()
    checkpoints.append(Checkpoint(CHECKPOINT_6_POINTS, CHECKPOINT_6_POINTS * int(passed6)))

    # Checkpoint 7: Assigned "Integrate with Kafka" to "Beta Release"
    passed7 = grade_checkpoint7()
    checkpoints.append(Checkpoint(CHECKPOINT_7_POINTS, CHECKPOINT_7_POINTS * int(passed7)))

    return result
