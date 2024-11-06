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


# check if the README.md contains the expected content
def check_readme_content1():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'api-server' not in content or 'http://the-agent-company.com:8929/root/api-server' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be an api-server repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content2():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'bustub' not in content or 'http://the-agent-company.com:8929/root/bustub' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a bustub repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content3():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'colly' not in content or 'http://the-agent-company.com:8929/root/colly' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a colly repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True


def check_readme_content4():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'janusgraph' not in content or 'http://the-agent-company.com:8929/root/janusgraph' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a janusgraph repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content5():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'llama.cpp' not in content or 'http://the-agent-company.com:8929/root/llama.cpp' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a llama.cpp repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True


def check_readme_content6():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'node-red' not in content or 'http://the-agent-company.com:8929/root/node-red' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a node-red repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True


def check_readme_content7():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'openhands' not in content or 'http://the-agent-company.com:8929/root/openhands' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a openhands repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content8():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'opensearch' not in content or 'http://the-agent-company.com:8929/root/opensearch' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a opensearch repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content9():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'raft' not in content or 'http://the-agent-company.com:8929/root/raft' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a raft repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content10():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'risingwave' not in content or 'http://the-agent-company.com:8929/root/risingwave' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a risingwave repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content11():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'sotopia' not in content or 'http://the-agent-company.com:8929/root/sotopia' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a sotopia repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True


def check_readme_content12():
    content = extract_readme_content()
    if content is None:
        return False
    
    if 'streamlit' not in content or 'http://the-agent-company.com:8929/root/streamlit' not in content:
        return False

    content_exists = evaluate_with_llm(
        content=content,
        predicate="there should be a streamlit repository link and one-sentence description (if either of the link, title name, or description is missing, this will be false; if all of these exist, this will be true)",
        additional_prompt="",
    )

    if not content_exists:
        logging.warning(f"README.md does not contain the expected content")
        return False

    return True

def check_readme_content13():
    content = extract_readme_content()
    if content is None:
        return False
    if 'contact' not in content or 'mikechen@example.com' not in content:
        return False
    else:
        return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []

    passed1 = check_readme_content1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = check_readme_content2()
    checkpoints.append(Checkpoint(2, int(passed2)))

    passed3 = check_readme_content3()
    checkpoints.append(Checkpoint(3, int(passed3)))

    passed4 = check_readme_content4()
    checkpoints.append(Checkpoint(4, int(passed4)))

    passed5 = check_readme_content5()
    checkpoints.append(Checkpoint(5, int(passed5)))

    passed6 = check_readme_content6()
    checkpoints.append(Checkpoint(6, int(passed6)))

    passed7 = check_readme_content7()
    checkpoints.append(Checkpoint(7, int(passed7)))

    passed8 = check_readme_content8()
    checkpoints.append(Checkpoint(8, int(passed8)))

    passed9 = check_readme_content9()
    checkpoints.append(Checkpoint(9, int(passed9)))

    passed10 = check_readme_content10()
    checkpoints.append(Checkpoint(10, int(passed10)))

    passed11 = check_readme_content11()
    checkpoints.append(Checkpoint(11, int(passed11)))

    passed12 = check_readme_content12()
    checkpoints.append(Checkpoint(12, int(passed12)))

    passed13 = check_readme_content13()
    checkpoints.append(Checkpoint(13, int(passed13)))

    return Result(checkpoints)
