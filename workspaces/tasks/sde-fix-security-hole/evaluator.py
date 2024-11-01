"""Evaluator for sde-fix-security-hole."""

import os
import sys
import logging
import requests
from typing import List

from common import get_chat_history, create_rocketchat_client
from scoring import Result, Checkpoint, bonus_for_completing_final

def grade_checkpoint1(trajectory=""):
    """The agent has communicated with Emily on RocketChat."""
    rocket = create_rocketchat_client()
    messages = get_chat_history(rocket, "Emily")
    return len(messages) > 0

def grade_checkpoint2(trajectory=""):
    """The agent has read event-viewer/README.md."""
    return "event-viewer/README.md" in trajectory

def grade_checkpoint3(trajectory=""):
    """The agent has run event-viewer/app.py."""
    return "python3 event-viewer/app.py" in trajectory or "python event-viewer/app.py" in trajectory

def grade_checkpoint4(trajectory=""):
    """The agent has communicated with Zhang on RocketChat."""
    rocket = create_rocketchat_client()
    messages = get_chat_history(rocket, "Zhang")
    return len(messages) > 0

def grade_checkpoint5():
    """app.py includes the word cat123."""
    try:
        with open('/workspace/TheAgentCompany/workspaces/tasks/sde-fix-security-hole/events-viewer/app.py', 'r') as file:
            content = file.read()
            return 'cat123' in content
    except FileNotFoundError:
        return False

def grade_checkpoint6():
    """The server returns events when accessed."""
    try:
        response = requests.get('http://localhost:5000/events')
        return response.status_code == 200 and len(response.json()) > 0
    except requests.RequestException:
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Define the scores corresponding to when each function is True
    scores = {
        lambda: grade_checkpoint1(trajectory): 1,
        lambda: grade_checkpoint2(trajectory): 1,
        lambda: grade_checkpoint3(trajectory): 1,
        lambda: grade_checkpoint4(trajectory): 1,
        grade_checkpoint5: 1,
        grade_checkpoint6: 1
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result
