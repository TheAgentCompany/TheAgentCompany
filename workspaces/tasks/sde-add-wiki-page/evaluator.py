import logging
import os
import sys
from typing import List
import urllib


from scoring import Result, Checkpoint
from common import make_gitlab_request, llm_complete
from config import GITLAB_BASEURL, GITLAB_USER
from prompts import wiki_evaluation_prompt

PROJECT_PATH = f"{GITLAB_USER}/sotopia"

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
    url = f"{GITLAB_BASEURL}/{PROJECT_PATH}"
    return url in trajectory

def grade_checkpoint2(wiki_page):
    return wiki_page is not None

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

    llm_response = llm_complete(messages)
    content = llm_response["choices"][0]["message"]["content"].lower().strip()
    return "yes" in content


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    wiki_page = get_wiki_page()

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_SCORE, CHECKPOINT_1_SCORE * int(passed1)))

    passed2 = grade_checkpoint2(wiki_page)
    checkpoints.append(Checkpoint(CHECKPOINT_2_SCORE, CHECKPOINT_2_SCORE * int(passed2)))

    passed3 = passed2 and grade_checkpoint3(wiki_page)
    checkpoints.append(Checkpoint(CHECKPOINT_3_SCORE, CHECKPOINT_3_SCORE * int(passed3)))

    return result


