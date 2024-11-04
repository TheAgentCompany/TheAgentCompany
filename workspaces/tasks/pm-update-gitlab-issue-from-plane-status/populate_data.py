import logging
from config import GITLAB_USER
from common import get_plane_project_id, make_gitlab_request

GITLAB_PROJECT_PATH=f"{GITLAB_USER}/openhands"

PLANE_PROJECT_NAME = "OpenHands"
PLANE_PROJECT_ID = get_plane_project_id(PLANE_PROJECT_NAME)
ISSUE_1 = "Model: recall rate is 0"
ISSUE_2 = "Model: security problem"


def create_issues_in_gitlab():
    issue1_exists = False
    issue1 = make_gitlab_request(GITLAB_PROJECT_PATH, "issues")
    issue1_exists = ISSUE_1 in [issue["title"] for issue in issue1.json()]
    if not issue1_exists:
        make_gitlab_request(GITLAB_PROJECT_PATH, "issues", method = "POST", params={"title": ISSUE_1})

    issue2_exists = False
    issue2 = make_gitlab_request(GITLAB_PROJECT_PATH, "issues")
    issue2_exists = ISSUE_2 in [issue["title"] for issue in issue2.json()]
    if not issue2_exists:
        make_gitlab_request(GITLAB_PROJECT_PATH, "issues", method = "POST", params={"title": ISSUE_2})
    return

if __name__ == "__main__":
    create_issues_in_gitlab()