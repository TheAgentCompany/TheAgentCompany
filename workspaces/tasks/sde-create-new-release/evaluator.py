import requests
import logging
import urllib

from typing import List

from scoring import Result, Checkpoint
from common import make_gitlab_request


############################# Init Variables #####################################
project_path = "root/risingwave"
release_path = "releases"
############################# Helper Functions #####################################

release_description = """
sql feature
Query syntax:
Public preview: Supports AS CHANGELOG to convert any stream into an append-only changelog.
SQL commands:
Breaking change: DECLARE cursor_name SUBSCRIPTION CURSOR is the same as DECLARE cursor_name SUBSCRIPTION CURSOR since now(), which will be consumed from the current time. DECLARE cursor_name SUBSCRIPTION CURSOR FULL will start consuming data from stock. The type of operation has changed to varchar. It is one of Insert, Delete, UpdateInset, or UpdateDelete.
"""

def check_release_content():
    total_point = 0

    release_encoded_path = urllib.parse.quote(release_path, safe='')
    try:
        releases = make_gitlab_request(project_path, release_encoded_path)
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking releases: {e}")
        return total_point

    if not releases:
        logging.warning("Release does not exist")
        return total_point

    most_recent_release = releases.json()[0]
    title = most_recent_release["name"]
    description = most_recent_release["description"]

    total_point = 0
    if title == "release-2024-10-12":
        total_point += 1
    
    if description.strip("\n").strip(" ") == release_description.strip("\n").strip(" "):
        total_point += 1

    return total_point


############################# Evaluator #####################################

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(2, int(check_release_content())))

    return result



