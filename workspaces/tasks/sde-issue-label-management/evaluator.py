import logging

from common import make_gitlab_request, get_gitlab_project_id, grader
from scoring import Result, Checkpoint, bonus_for_completing_final

PROJECT_NAME = "sotopia"
BUG_ISSUE_IID = 200
NON_BUG_ISSUE_IID = 140  # This issue doesn't have `bug` in its title but has a `bug` label

@grader
def check_issue(issue_iid: int):
    project_id = get_gitlab_project_id(PROJECT_NAME)
    if project_id is None:
        logging.error(f"Project {PROJECT_NAME} not found")
        return False

    resp = make_gitlab_request(project_id, additional_path=f"issues/{issue_iid}")
    if resp is None:
        logging.error(f"Issue {issue_iid} not found")
        return False
    issue = resp.json()
    
    labels = [label.lower() for label in issue.get("labels", [])]

    if "bug" in issue["title"].lower() and "bug" not in labels:
        logging.error(f"Issue {issue['title']} does not have a 'bug' label")
        return False

    elif "bug" not in issue["title"].lower() and "bug" in labels:
        logging.error(f"Issue {issue['title']} shouldn't have a 'bug' label")
        return False
    
    return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(1, 1*int(check_issue(BUG_ISSUE_IID) and check_issue(NON_BUG_ISSUE_IID)))
    return Result([checkpoint1], bonus_for_completing_final)
