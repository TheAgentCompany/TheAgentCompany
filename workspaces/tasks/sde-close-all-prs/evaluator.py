import logging
from typing import List

from scoring import Result, Checkpoint
from common import *


@checkpoint
def grade_checkpoint1():
    try:
        # Get all projects
        response = make_gitlab_request(additional_path="projects").json()

        if len(response) == 0:
            logging.warning(f"All repositories are deleted.")
            return False

        for repo in response:
            repo_name = repo["name"]
            repo_id = str(repo["id"])
            merge_requests = make_gitlab_request(project_identifier=repo_id, additional_path="merge_requests", params={"state": "opened"}).json()
            if len(merge_requests) > 0:
                logging.warning(f"Some PRs are not closed in repository {repo_name}.")
                return False

        return True

    except Exception as e:
        logging.error(f"Error occurred while checking the repository", exc_info=True)
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(2, 2 * int(grade_checkpoint1())))

    return result
