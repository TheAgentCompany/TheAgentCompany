import logging
import requests
import urllib.parse
import base64
from typing import List
import json

from common import make_gitlab_request, evaluate_with_llm, checkpoint
from scoring import Result, Checkpoint

project_path = "root/api-server"
target_title = "## Contribute to this project"


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


# check if the README.md contains the expected title
@checkpoint
def check_readme_title():
    content = extract_readme_content()
    if content is None:
        return False

    if target_title in content:
        logging.info(f"README.md contains the title '{target_title}'")
        return True
    else:
        logging.warning(f"README.md does not contain the title '{target_title}'")
        return False


# check if the README.md contains the expected content
@checkpoint
def check_readme_content():
    content = extract_readme_content()
    if content is None:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there are **contents** regarding contributing to the project (if only the title is present, this will be false; but if only the content is present, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    passed1 = check_readme_title()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = check_readme_content()
    checkpoints.append(Checkpoint(1, int(passed2)))

    return Result(checkpoints)
