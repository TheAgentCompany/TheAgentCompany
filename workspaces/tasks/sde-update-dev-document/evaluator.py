"""
Evaluator for the task <Delete all Rocket.Chat channels>
"""

import os
import logging
from typing import List

from common import get_gitlab_project_id, get_gitlab_merge_request_by_title, get_gitlab_file_in_mr
from scoring import Result, Checkpoint, bonus_for_completing_final


PROJECT_NAME = "sotopia"
DOC_PATH = "docs/pages/contribution/contribution.md"
MR_TITLE = "Update contribution document"

def validate_doc(doc: str):
    doc = doc.lower()
    for keyword in ["using vscode", "other ides or editors", "without dev container"]:
        if keyword not in doc:
            return False
    return True

def grade_checkpoint1():
    # check if local doc file passes the validation
    if not os.path.exists(os.path.join(PROJECT_NAME, DOC_PATH)):
        return False
    with open(os.path.join(PROJECT_NAME, DOC_PATH), "r") as f:
        doc = f.read()
        return validate_doc(doc)

def grade_checkpoint2():
    # check if MR is posted and the doc passes the validation
    project_id = get_gitlab_project_id(PROJECT_NAME)
    if project_id is None:
        return False
    mr = get_gitlab_merge_request_by_title(project_id, MR_TITLE)
    if mr is None:
        return False
    doc = get_gitlab_file_in_mr(mr, DOC_PATH)
    if doc is None:
        return False
    return validate_doc(doc)


def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(3, 3*int(grade_checkpoint1()))
    checkpoint2 = Checkpoint(1, 1*int(grade_checkpoint2()))
    return Result([checkpoint1, checkpoint2], bonus_for_completing_final)
