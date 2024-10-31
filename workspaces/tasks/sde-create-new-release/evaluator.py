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

def get_most_recent_release():
    release_encoded_path = urllib.parse.quote(release_path, safe='')
    try:
        releases = make_gitlab_request(project_path, release_encoded_path)
    except requests.RequestException as e:
        logging.error(f"Error occurred while checking releases: {e}")
        return None

    if not releases:
        logging.warning("Release does not exist")
        return None
    return releases.json()[0]


def check_release_title():
    most_recent_release = get_most_recent_release()
    if most_recent_release is None:
        return False
    if most_recent_release['title'] == "release-2024-10-12":
        return True
    return False

def check_release_content():
    most_recent_release = get_most_recent_release()
    if most_recent_release is None:
        return False

    description = most_recent_release["description"]

    if description.strip("\n").strip(" ") == release_description.strip("\n").strip(" "):
        return True
    return False


############################# Evaluator #####################################

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(check_release_content())))

    checkpoints.append(Checkpoint(1, int(check_release_content())))

    return result



