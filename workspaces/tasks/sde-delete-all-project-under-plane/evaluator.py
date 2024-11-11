import requests
import logging

from typing import List

from scoring import Result, Checkpoint
from common import *


# all project get deleted.
@grader
def grade_checkpoint1():
    try:
        # get all projects
        projects = get_all_plane_projects()

        if len(projects) != 0:
            all_project_names = [project["name"] for project in projects]
            logging.warning(
                f"Projects are not deleted, existing projects: {all_project_names}"
            )
            return False

        return True

    except Exception as e:
        logging.error(f"Error fetching branch data: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, grade_checkpoint1()))
    return result



