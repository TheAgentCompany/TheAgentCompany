"""Evaluator for sde-fix-security-hole."""

import os
import sys
import logging
import sqlite3
import unittest
from typing import List

from common import get_chat_history, create_rocketchat_client
from scoring import Result, Checkpoint

def grade_checkpoint1(trajectory=""):
    """The agent has communicated with Emily on RocketChat."""
    rocket = create_rocketchat_client()
    messages = get_chat_history(rocket, "Emily Zhou")
    return len(messages) > 0

def grade_checkpoint2():
    """The agent has added a test for incorrect password."""
    try:
        with open('/workspace/TheAgentCompany/workspaces/tasks/sde-fix-security-hole/events-viewer/test_app.py', 'r') as file:
            content = file.read()
            return 'test_incorrect_password' in content and 'wrong_password' in content
    except FileNotFoundError:
        return False

def grade_checkpoint3():
    """The agent has fixed app.py."""
    try:
        with open('/workspace/TheAgentCompany/workspaces/tasks/sde-fix-security-hole/events-viewer/app.py', 'r') as file:
            content = file.read()
            return 'PRAGMA key' in content and 'get_db' in content
    except FileNotFoundError:
        return False

def grade_checkpoint4():
    """The agent has fixed populate_database.py."""
    try:
        with open('/workspace/TheAgentCompany/workspaces/tasks/sde-fix-security-hole/events-viewer/populate_database.py', 'r') as file:
            content = file.read()
            return 'PRAGMA key' in content and 'get_db' in content
    except FileNotFoundError:
        return False

def grade_checkpoint5():
    """All tests pass."""
    try:
        # Create a test database
        db = sqlite3.connect(':memory:')
        db.execute("PRAGMA key='cat123'")
        db.execute('''
            CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        db.execute("INSERT INTO events (name, date, description) VALUES (?, ?, ?)",
                  ('Test Event', '2024-01-01', 'Test Description'))
        db.commit()
        db.close()

        # Run the tests
        loader = unittest.TestLoader()
        tests = loader.discover('/workspace/TheAgentCompany/workspaces/tasks/sde-fix-security-hole/events-viewer', pattern='test_*.py')
        runner = unittest.TextTestRunner()
        result = runner.run(tests)
        return result.wasSuccessful()
    except:
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        lambda: grade_checkpoint1(trajectory): 1,
        grade_checkpoint2: 2,
        grade_checkpoint3: 2,
        grade_checkpoint4: 2,
        grade_checkpoint5: 3
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result
