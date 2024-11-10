"""
Evaluator for the task <Delete all Rocket.Chat channels>
"""

import logging
from typing import List

from common import make_gitlab_request
from scoring import Result, Checkpoint, bonus_for_completing_final

def grade_checkpoint1():
    page_index = 1
    while True:
        resp = make_gitlab_request(additional_path=f"projects?page={page_index}&per_page=100")
        if resp is None:
            return False
        projects = resp.json()
        for project in projects:
            project_detail_resp = make_gitlab_request(str(project['id']))
            if project_detail_resp is None:
                return False
            open_issues_count = project_detail_resp.json().get('open_issues_count', 0)
            if open_issues_count > 0:
                logging.info(f"Found an issue in project {project['name']}")
                return False
        if len(projects) < 100:
            break
        page_index += 1

    return True

def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(2, 2*int(grade_checkpoint1()))
    return Result([checkpoint1], bonus_for_completing_final)
