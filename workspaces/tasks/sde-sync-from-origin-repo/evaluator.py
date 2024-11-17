import requests
import logging
import urllib

from typing import List

from scoring import Result, Checkpoint
from common import *

project_path = "root/janusgraph"
file_path = "janusgraph-dist/pom.xml"
target_keyword = "<docker.build.skip>"

def get_file_content():
    encoded_file_path = urllib.parse.quote(file_path, safe='')
    try:
        response = make_gitlab_request(project_path, f"repository/files/{encoded_file_path}/raw")
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        logging.error(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response content'}")
        return ""
    except Exception as e:
        logging.error(f"Failed to fetch file content: {e}")
        return ""

# Check if the docker.build.skip keyword exists in the pom.xml file.
@grader
def grade_checkpoint1():
    try:
        content = get_file_content()
        if not content:
            logging.error("Failed to get file content")
            return False
        has_keyword = target_keyword in content
        return has_keyword
    except Exception as e:
        logging.error(f"Checkpoint evaluation failed: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    return result



