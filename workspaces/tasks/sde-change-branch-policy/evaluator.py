import requests
import logging

base_url = "http://the-agent-company.com:8929/api/v4"
project_id = "root%2Fsotopia"
access_token = "root-token"
headers = {"PRIVATE-TOKEN": access_token}


def grade_checkpoint1():
    # check the `allowed to merge` is only for `maintainers`
    branch_url = f"{base_url}/projects/{project_id}/protected_branches"
    try:
        response = requests.get(branch_url, headers=headers)
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


def grade_checkpoint2():
    # check `allowed to merge and push` is changed to `maintainers and developers`
    branch_url = f"{base_url}/projects/{project_id}/protected_branches"
    try:
        response = requests.get(branch_url, headers=headers)
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
