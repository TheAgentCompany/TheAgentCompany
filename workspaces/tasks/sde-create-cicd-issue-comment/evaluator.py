"""Evaluator for sde-create-cicd-issue-comment."""

import sys
import logging
from typing import List

from common import make_gitlab_request
from scoring import Result, Checkpoint, bonus_for_completing_final

# Configuration for gitlab
project_path = "janusgraph/janusgraph"

def grade_checkpoint1():
    """Sent a merge request to add the CI/CD action."""
    # Get merge requests
    response = make_gitlab_request(project_path, "merge_requests?state=opened")
    if response is None:
        return False
    
    merge_requests = response.json()
    if not merge_requests:
        return False

    # Look for MR with CI/CD action
    for mr in merge_requests:
        if "comment formatting" in mr['title']:
            # Get the MR changes
            mr_iid = mr['iid']
            changes_response = make_gitlab_request(project_path, f"merge_requests/{mr_iid}/changes")
            if changes_response is None:
                continue
                
            changes = changes_response.json()
            for change in changes.get('changes', []):
                if '.gitlab-ci.yml' in change['new_path']:
                    return True
                
    return False

def grade_checkpoint2():
    """Merge the merge request."""
    response = make_gitlab_request(project_path, "merge_requests?state=opened")
    if response is None:
        return False
    
    merge_requests = response.json()
    if not merge_requests:
        return False
    
    # Look for MR with CI/CD action
    for mr in merge_requests:
        if "comment formatting" in mr['title']:
            return mr['state'] == "merged"

def grade_checkpoint3():
    """Opened an issue with a title that doesn't start with "fix:", "chore:", or "feat:", and verified that the CI/CD action comments."""
    # Get the most recent issue
    response = make_gitlab_request(project_path, "issues?sort=desc")
    if response is None:
        return False
    
    issues = response.json()
    if not issues:
        return False
    
    # Find the "Dummy Issue"
    for issue in issues:
        if issue['title'] == "Dummy Issue 1":
            # Get issue comments
            issue_iid = issue['iid']
            comments_response = make_gitlab_request(project_path, f"issues/{issue_iid}/notes")
            if comments_response is None:
                continue
            
            comments = comments_response.json()
            for comment in comments:
                if "All issue titles must start with 'fix:', 'chore:', or 'feat:'" in comment['body']:
                    return True
    
    return False

def grade_checkpoint4():
    """Opened an issue with a body less than 100 characters, and verified that the CI/CD action comments."""
    # Get the most recent issues
    response = make_gitlab_request(project_path, "issues?sort=desc")
    if response is None:
        return False
    
    issues = response.json()
    if not issues:
        return False
    
    # Find an issue with a title that starts with fix:, chore:, or feat:
    for issue in issues:
        if issue['title'] == "fix: Dummy Issue 2":
            # Get issue comments
            issue_iid = issue['iid']
            comments_response = make_gitlab_request(project_path, f"issues/{issue_iid}/notes")
            if comments_response is None:
                continue

            # Check if the issue has a body of at least 100 characters
            if len(issue['body']) < 100:
                return True
            
            comments = comments_response.json()
            for comment in comments:
                if "All issues must have a body at least 100 characters long" in comment['body']:
                    return True
    
    return False

def grade_checkpoints() -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 1,
        grade_checkpoint4: 1,
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result
