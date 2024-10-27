import requests
import logging
from common import *

project_path = "root/sotopia"

# check the `allowed to merge` is only for `maintainers`
def grade_checkpoint1():
    try:
        response = make_gitlab_request(project_path, "protected_branches")
        response.raise_for_status()
        data = response.json()
        for branch in data:
            if branch["name"] == "main":
                if branch["merge_access_levels"][0]["access_level"] != 30:
                    logging.warning(
                        f"`Allowed to merge` is not set to `maintainers and developers`, now {branch['merge_access_levels'][0]['access_level_description']}"
                    )
                    return False
                return True

        logging.warning("Main branch is not protected")
        return False

    except Exception as e:
        logging.error(f"Error fetching branch data: {e}")
        return False

# check `allowed to merge and push` is changed to `maintainers and developers`
def grade_checkpoint2():
    try:
        response = make_gitlab_request(project_path, "protected_branches")
        response.raise_for_status()
        data = response.json()
        for branch in data:
            if branch["name"] == "main":
                if branch["push_access_levels"][0]["access_level"] != 0:
                    logging.warning(
                        f"`Allowed to merge and push` is not set to `no one`, now {branch['merge_access_levels'][0]['access_level_description']}"
                    )
                    return False
                return True

        logging.warning("Main branch is not protected")
        return False

    except Exception as e:
        logging.error(f"Error fetching branch data: {e}")
        return False


if __name__ == "__main__":
    passed1 = grade_checkpoint1()
    passed2 = grade_checkpoint2()
    print(f"Final points for task: {passed1 + passed2}")
