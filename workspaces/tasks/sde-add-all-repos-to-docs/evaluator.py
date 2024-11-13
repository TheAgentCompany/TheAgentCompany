import logging
import urllib.parse
from typing import List
import re

from scoring import Result, Checkpoint
from common import make_gitlab_request
from config import GITLAB_USER, GITLAB_BASEURL

CHECKPOINT_1_POINTS = 2
CHECKPOINT_2_POINTS = 1

PROJECT_NAME = 'Documentation'
PROJECT_PATH = f"{GITLAB_USER}/doc"
README_FILE_PATH = 'README.md'
EMAIL = "mike.chen@agentcompany.com"

def get_readme_content():
    # Get README.md content from 'doc' repository
    encoded_file_path = urllib.parse.quote(README_FILE_PATH, safe='')
    response = make_gitlab_request(
        PROJECT_PATH,
        f'repository/files/{encoded_file_path}/raw',
        params={'ref': 'main'}
    )
    if response is None or response.status_code != 200:
        logging.error('Failed to fetch README.md from doc repository')
        return ''
    return response.text

def grade_checkpoint1(readme_content, projects):
    for project in projects:
        project_name = project.get('name')
        project_url = GITLAB_BASEURL + '/root/' + project_name
        if project_name and project_url:
            # Check if the README contains the project name and link
            if not (project_name in readme_content and project_url in readme_content):
                return False
    return True

def grade_checkpoint2(readme_content):
    # Check if the contact section with Mike Chen's information is included at the bottom
    return EMAIL in readme_content

def grade_checkpoints(trajectory='') -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    projects = make_gitlab_request(None, 'projects').json()
    readme_content = get_readme_content()

    # Remove the 'doc' repository itself from the list
    projects = [project for project in projects if project.get('name') != PROJECT_NAME]

    # Checkpoint 1: Check if the agent correctly puts in each repo's information
    passed_checkpoint1 = grade_checkpoint1(readme_content, projects)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed_checkpoint1)))

    # Checkpoint 2: Check if the readme contains a contact section with Mike Chen's information
    passed_checkpoint2 = grade_checkpoint2(readme_content)
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed_checkpoint2)))

    return result
