import logging

from common import get_gitlab_project_id, make_gitlab_request

PROJECT_NAME = "sotopia"

def no_avatar_set_for_project():
    project_id = get_gitlab_project_id(PROJECT_NAME)
    if project_id is None:
        raise Exception(f"Project {PROJECT_NAME} not found")
    project_resp = make_gitlab_request(project_id)
    if project_resp is None:
        raise Exception(f"Failed to get project {PROJECT_NAME}")
    project = project_resp.json()
    if project.get("avatar_url") is not None:
        raise Exception(f"Avatar shouldn't be set for the project {PROJECT_NAME}")
    return

if __name__ == "__main__":
    no_avatar_set_for_project()
