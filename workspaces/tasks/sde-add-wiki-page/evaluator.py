"""Summary of evaluator for example task

You don't have to write a summary for the evaluator, although documentation is
strongly encouraged.

A good evaluator should:
1. be robust - it shouldn't abort because of its own bug or lack of fail over mechanism
2. be deterministic and idempotent
3. grant partial credits if possible
4. encourage but not require trajectory for grading
"""
import logging
import os
import sys
from common import *
import urllib
import json
from prompts import wiki_evaluation_prompt

SERVER_HOSTNAME = 'the-agent-company.com'
GITLAB_PORT = '8929'
GITLAB_USER = "root"
GITLAB_URL = f"http://{SERVER_HOSTNAME}:{GITLAB_PORT}/{GITLAB_USER}"
PROJECT_NAME = "sotopia"
PROJECT_PATH = f"{GITLAB_USER}/{PROJECT_NAME}"

CHECKPOINT_1_SCORE = 1
CHECKPOINT_2_SCORE = 1
CHECKPOINT_3_SCORE = 2

README_PATH = "README.md"

def get_wiki_page():
    try:
        response = make_gitlab_request(PROJECT_PATH, "wikis?with_content=1")
        response.raise_for_status()
        data = response.json()
        if len(data) == 0:
            return None
        return data[0]
    except Exception as e:
        logging.error(f"Error fetching wiki page: {e}")
        return None
    
def get_readme():
    readme_encoded_path = urllib.parse.quote(README_PATH, safe='')
    try:
        response = make_gitlab_request(PROJECT_PATH, f"repository/files/{readme_encoded_path}/raw?ref=main")
        response.raise_for_status()
        return response.text
    except Exception as e:
        logging.error(f"Error fetching README: {e}")
        return None

def grade_checkpoint1(trajectory):
    url = f"{GITLAB_URL}/{PROJECT_NAME}"
    return url in trajectory

def grade_checkpoint2(wiki_page):
    if wiki_page is None:
        return False
    return True

def grade_checkpoint3(wiki_page):
    wiki = f"{json.dumps(wiki_page)}"
    readme = get_readme()
    if readme is None:
        return False
    messages = [
        {
            "role": "user",
            "content": wiki_evaluation_prompt.substitute(wiki=wiki, readme=readme)
        }
    ]

    llm_response = llm_evaluate(messages)
    content = llm_response["choices"][0]["message"]["content"].lower().strip()
    return "yes" in content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, partial credit might not be granted")
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)

    wiki_page = get_wiki_page()

    passed1 = grade_checkpoint1(trajectory)
    passed2 = grade_checkpoint2(wiki_page)
    if not passed2:
        passed3 = False
    else:
        passed3 = grade_checkpoint3(wiki_page)
    points = CHECKPOINT_1_SCORE * int(passed1) + CHECKPOINT_2_SCORE * int(passed2) + CHECKPOINT_3_SCORE * int(passed3)
    print(f"Final points for task 'sde-add-wiki-page': {points}")
