import logging
import urllib.parse
from typing import List
import re

from scoring import Result, Checkpoint
from common import make_gitlab_request, grader
from config import GITLAB_USER, GITLAB_BASEURL

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1
CHECKPOINT_3_POINTS = 1


PROJECT_NAME = 'Documentation'
PROJECT_PATH = f"{GITLAB_USER}/doc"
README_FILE_PATH = 'README.md'
EMAIL = "mike.chen@agentcompany.com"

DESCRIPTIONS = {
    "api-server": "REST APIs for internal use.",
    "bustub": "The BusTub Relational Database Management System.",
    "colly": "Elegant Scraper and Crawler Framework for Golang.",
    "copilot-arena-server": "Support server for Copilot Arena.",
    "janusgraph": "JanusGraph: An open-source, distributed graph database.",
    "llama.cpp": "LLM inference in C/C++.",
    "node-red": "Low-code programming for event-driven applications.",
    "openhands": "OpenHands: Code Less, Make More.",
    "opensearch": "Open source distributed and RESTful search engine.",
    "raft": "Implementation of the Raft consensus algorithm.",
    "risingwave": "Unified streaming and batch. PostgreSQL-compatible stream processing, real-time ETL pipelines, and feature stores.",
    "sotopia": "Sotopia: An open-ended social learning environment (ICLR 2024 spotlight).",
    "streamlit": "Streamlit — A faster way to build and share data apps."
}

def get_projects():
    response = make_gitlab_request(None, 'projects')
    if response is None or response.status_code != 200:
        logging.error('Failed to fetch projects from GitLab')
        return []
    projects = response.json()
    if projects is None:
        logging.error('Failed to fetch projects from GitLab')
        return []
    return projects

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

@grader
def grade_checkpoint1(readme_content, projects):
    if projects is None or len(projects) == 0:
        logging.error('No projects found')
        return False
    for project in projects:
        project_name = project.get('name')
        project_url = GITLAB_BASEURL + '/root/' + project_name
        if project_name and project_url:
            # Check if the README contains the project name and link
            if not (project_name in readme_content and project_url in readme_content):
                return False
    return True

@grader
def grade_checkpoint2(readme_content, projects):
    # check if the descriptions are included in the README
    for project in projects:
        project_name = project.get('name')
        project_description = DESCRIPTIONS.get(project_name)
        if project_name and project_description:
            if not project_description in readme_content:
                return False
    return True

@grader
def grade_checkpoint3(readme_content):
    # Check if the contact section with Mike Chen's information is included at the bottom
    return EMAIL in readme_content

def grade_checkpoints(trajectory='') -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    projects = get_projects()
    readme_content = get_readme_content()

    # Remove the 'doc' repository itself from the list
    projects = [project for project in projects if project.get('name') != PROJECT_NAME]

    # Checkpoint 1: Check if the agent correctly puts in each repo's information
    passed_checkpoint1 = grade_checkpoint1(readme_content, projects)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed_checkpoint1)))

    # Checkpoint 2: Check if the descriptions are included in the README
    passed_checkpoint2 = grade_checkpoint2(readme_content, projects)
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed_checkpoint2)))

    # Checkpoint 3: Check if the readme contains a contact section with Mike Chen's information
    passed_checkpoint3 = grade_checkpoint3(readme_content)
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, CHECKPOINT_3_POINTS * int(passed_checkpoint3)))

    return result
