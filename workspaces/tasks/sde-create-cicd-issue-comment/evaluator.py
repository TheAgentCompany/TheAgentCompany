"""Evaluator for sde-create-cicd-issue-comment."""

import sys
import logging
from typing import List

from common import make_gitlab_request
from scoring import Result, Checkpoint, bonus_for_completing_final

# Configuration for gitlab
project_path = "janusgraph/janusgraph"

def grade_checkpoint1(trajectory=""):
    """Opened JanusGraph's gitlab repository."""
    keywords = ["https://gitlab.com/janusgraph/janusgraph", ".gitlab-ci.yml", "issue_title", "issue_body"]
    return all(keyword in trajectory for keyword in keywords)

def grade_checkpoint2(trajectory=""):
    """Sent a merge request to add the CI/CD action."""
    return "new branch" in trajectory.lower() and "merge request" in trajectory.lower()

def grade_checkpoint3(trajectory=""):
    """Requested review from Li, and once approved, merged the merge request."""
    return "request review from Li" in trajectory.lower() and "approved" in trajectory.lower() and "merge" in trajectory.lower()

def grade_checkpoint4():
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
        if issue['title'] == "Dummy Issue":
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

def grade_checkpoint5():
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
        if any(issue['title'].startswith(prefix) for prefix in ["fix:", "chore:", "feat:"]):
            # Get issue comments
            issue_iid = issue['iid']
            comments_response = make_gitlab_request(project_path, f"issues/{issue_iid}/notes")
            if comments_response is None:
                continue
            
            comments = comments_response.json()
            for comment in comments:
                if "All issues must have a body at least 100 characters long" in comment['body']:
                    return True
    
    return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Define the scores corresponding to when each function is True
    scores = {
        lambda: grade_checkpoint1(trajectory): 1,
        lambda: grade_checkpoint2(trajectory): 1,
        lambda: grade_checkpoint3(trajectory): 1,
        grade_checkpoint4: 1,
        grade_checkpoint5: 1
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result
