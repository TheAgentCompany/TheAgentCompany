import logging
import requests
import urllib.parse
import base64
from typing import List
import json

from common import make_gitlab_request, evaluate_with_llm
from scoring import Result, Checkpoint

project_path = "root/doc"


def extract_readme_content():
    try:
        response = make_gitlab_request(
            project_identifier=project_path,
            additional_path="repository/files/README.md?ref=main",
        )
        if not response:
            return None
        response_data = response.json()

        if response.status_code == 200:
            content = response_data.get("content", "")
            # decode the base64 encoded content
            content = base64.b64decode(content).decode("utf-8")
            return content
        else:
            logging.warning(f"Unexpected status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Error occurred while extracting the README.md content: {e}")
        return None


def check_readme_content_repo(repo_name, link):
    content = extract_readme_content()
    if content is None:
        return False
    
    if repo_name not in content or link not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate=f"there should be a {repo_name} repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content_contact():
    content = extract_readme_content()
    if content is None:
        return False
    if 'mikechen@example.com' not in content:
        return False
    else:
        return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []

    passed1 = check_readme_content_repo('api-server', 'http://the-agent-company.com:8929/root/api-server')
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = check_readme_content_repo('bustub', 'http://the-agent-company.com:8929/root/bustub')
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = check_readme_content_repo('colly',  'http://the-agent-company.com:8929/root/colly')
    checkpoints.append(Checkpoint(1, int(passed3)))

    passed4 = check_readme_content_repo('janusgraph',  'http://the-agent-company.com:8929/root/janusgraph')
    checkpoints.append(Checkpoint(1, int(passed4)))

    passed5 = check_readme_content_repo('llama.cpp',  'http://the-agent-company.com:8929/root/llama.cpp')
    checkpoints.append(Checkpoint(1, int(passed5)))

    passed6 = check_readme_content_repo('node-red',  'http://the-agent-company.com:8929/root/node-red')
    checkpoints.append(Checkpoint(1, int(passed6)))

    passed7 = check_readme_content_repo('openhands',  'http://the-agent-company.com:8929/root/openhands')
    checkpoints.append(Checkpoint(1, int(passed7)))

    passed8 = check_readme_content_repo('opensearch',  'http://the-agent-company.com:8929/root/opensearch')
    checkpoints.append(Checkpoint(1, int(passed8)))

    passed9 = check_readme_content_repo('raft',  'http://the-agent-company.com:8929/root/raft')
    checkpoints.append(Checkpoint(1, int(passed9)))

    passed10 = check_readme_content_repo('risingwave',  'http://the-agent-company.com:8929/root/risingwave')
    checkpoints.append(Checkpoint(1, int(passed10)))

    passed11 = check_readme_content_repo('sotopia',  'http://the-agent-company.com:8929/root/sotopia')
    checkpoints.append(Checkpoint(1, int(passed11)))

    passed12 = check_readme_content_repo('streamlit',  'http://the-agent-company.com:8929/root/streamlit')
    checkpoints.append(Checkpoint(1, int(passed12)))

    passed13 = check_readme_content_contact()
    checkpoints.append(Checkpoint(1, int(passed13)))

    return Result(checkpoints)

