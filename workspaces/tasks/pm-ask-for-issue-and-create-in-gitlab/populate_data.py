from config import GITLAB_USER
from common import make_gitlab_request

GITLAB_PROJECT_PATH=f"{GITLAB_USER}/risingwave"

MILESTONE = "Alpha Release"

def create_milestone_in_gitlab():
    milestone_exists = False
    milestone = make_gitlab_request(GITLAB_PROJECT_PATH, "milestones")
    if milestone is not None:
        milestone_exists = MILESTONE in [milestone["title"] for milestone in milestone.json()]
        if not milestone_exists:
            make_gitlab_request(GITLAB_PROJECT_PATH, "milestones", method = "POST", params={"title": MILESTONE})
    return

if __name__ == "__main__":
    create_milestone_in_gitlab()