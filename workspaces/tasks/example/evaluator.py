"""Summary of evaluator for example task

You don't have to write a summary for the evaluator, although documentation is
strongly encouraged.

A good evaluator should:
1. be robust - it shouldn't abort because of its own bug or lack of fail over mechanism
2. be deterministic and idempotent
3. grant partial credits if possible
4. encourage but not require trajectory for grading
"""

import requests
import logging
import os
import sys
from common import llm_evaluate

def grade_checkpoint1(trajectory):
    return "8929/root/api-server" in trajectory

def grade_checkpoint2():
    if os.path.exists('/workspace/api-server/server.py'):
        with open('/workspace/api-server/server.py') as f:
            code_content = f.read()
            if "Welcome to the Flask API" in code_content:
                return True
    return False

def grade_final_checkpoint():
    try:
        response = requests.get("http://localhost:5432/welcome")
        return response.status_code == 200 and response.json() == {"message": "Welcome to the Flask API!"}
    except Exception:
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

    passed1 = grade_checkpoint1(trajectory)
    passed2 = grade_checkpoint2()
    passed3 = grade_final_checkpoint()
    points = 4 if passed3 else int(passed1) + int(passed2)
    print(f"Final points for task Example: {points}")
