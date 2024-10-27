import requests
import logging
from common import *

project_path = "root/sotopia"


# all project get deleted.
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


if __name__ == "__main__":
    passed1 = int(grade_checkpoint1())
    print(f"Final points for task: {passed1}")
