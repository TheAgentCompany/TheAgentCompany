"""Evaluator for sde-create-cicd-issue-comment."""

import os
import sys
import logging
import requests

def grade_checkpoint1(trajectory):
    keywords = ["https://gitlab.com/janusgraph/janusgraph", ".gitlab-ci.yml", "issue_title", "issue_body"]
    return all(keyword in trajectory for keyword in keywords)

def grade_checkpoint2(trajectory):
    return "new branch" in trajectory.lower() and "merge request" in trajectory.lower()

def grade_checkpoint3(trajectory):
    return "request review from Li" in trajectory.lower() and "approved" in trajectory.lower() and "merge" in trajectory.lower()

def grade_checkpoint4(trajectory):
    keywords = ['"Dummy Issue"', "more than 100 characters", "All issue titles must start with"]
    return all(keyword in trajectory for keyword in keywords)

def grade_checkpoint5(trajectory):
    keywords = ["fix:", "chore:", "feat:", "less than 100 characters", "All issues must have a body at least 100 characters long"]
    return any(keyword in trajectory for keyword in keywords[:3]) and all(keyword in trajectory for keyword in keywords[3:])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, partial credit might not be granted")
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)

    points = sum([
        grade_checkpoint1(trajectory),
        grade_checkpoint2(trajectory),
        grade_checkpoint3(trajectory),
        grade_checkpoint4(trajectory),
        grade_checkpoint5(trajectory)
    ])

    print(f"Final points for task: {points}")
