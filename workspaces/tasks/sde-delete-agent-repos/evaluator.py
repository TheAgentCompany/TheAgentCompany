import logging
from typing import List

from scoring import Result, Checkpoint
from common import make_gitlab_request


def check_no_agent_repos(response: list) -> list:
    remaining_repos = []
    if any(["openhands" in repo["name"] for repo in response]):
        remaining_repos.append("openhands")
    if any(["sotopia" in repo["name"] for repo in response]):
        remaining_repos.append("sotopia")
    return remaining_repos


def check_agent_repos_deleted():
    try:
        # Get all projects
        response = make_gitlab_request(additional_path="projects").json()
        remaining_repos = [repo["name"] for repo in response]

        if len(remaining_repos) == 0 and len(response) == 12:
            logging.info(f"All repositories are deleted.")
            return True
        else:
            logging.warning(f"Some repositories are not deleted: {remaining_repos}")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, int(check_agent_repos_deleted())))
    return result