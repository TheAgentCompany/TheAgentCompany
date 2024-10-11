"""Evaluator for sde-debug-crashed-server."""

import os
import sys
import logging
import re
import requests

def grade_checkpoint1(trajectory):
    return "Emily" in trajectory and "RocketChat" in trajectory

def grade_checkpoint2(trajectory):
    return "ssh" in trajectory

def grade_checkpoint3():
    return os.path.exists('/workspace/pr-viewer/README.md')

def grade_checkpoint4():
    return os.path.exists('/workspace/pr-viewer/logs/gunicorn.log')

def grade_checkpoint5(trajectory):
    return "Zhang" in trajectory and "RocketChat" in trajectory

def grade_checkpoint6():
    try:
        with open('/workspace/pr-viewer/config.toml', 'r') as file:
            content = file.read()
            return bool(re.search(r'db_password.*dbcat456', content))
    except FileNotFoundError:
        return False

def grade_checkpoint7():
    try:
        response = requests.get('http://localhost:5000/')
        return "pr-viewer" in response.text.lower()
    except requests.RequestException:
        return False

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
        grade_checkpoint3(),
        grade_checkpoint4(),
        grade_checkpoint5(trajectory),
        grade_checkpoint6(),
        grade_checkpoint7()
    ])

    print(f"Final points for task: {points}")
