import logging

from common import make_gitlab_request, get_gitlab_project_id

PROJECT_NAME = "sotopia"
BUG_ISSUE_IID = 200
NON_BUG_ISSUE_IID = 140  # This issue doesn't have `bug` in its title but has a `bug` label


def issue_exists(issue_iid: int, bug_in_title: bool, has_bug_label: bool):
    project_id = get_gitlab_project_id(PROJECT_NAME)
    if project_id is None:
        raise Exception(f"Project {PROJECT_NAME} not found")

    resp = make_gitlab_request(project_id, additional_path=f"issues/{issue_iid}")
    if resp is None:
        raise Exception(f"Issue {issue_iid} not found")
    issue = resp.json()
    
    if bug_in_title and "bug" not in issue["title"].lower():
        raise Exception(f"Issue {issue['title']} does not contain 'bug' in its title")

    if has_bug_label and "bug" not in [label.lower() for label in issue.get("labels", [])]:
        raise Exception(f"Issue {issue['title']} does not have a 'bug' label")
    
    return


if __name__ == "__main__":
    issue_exists(BUG_ISSUE_IID, True, True)
    issue_exists(NON_BUG_ISSUE_IID, False, True)
