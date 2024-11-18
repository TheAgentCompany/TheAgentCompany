import os
import subprocess
from typing import List
import logging

from scoring import Result, Checkpoint
from common import grader

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 1

OPENHANDS_REPO_PATH = '/workspace/openhands'

# Lines to check for double quotes in specific files
FILES_TO_CHECK = {
    'evaluation/agent_bench/helper.py': [
        'raw_ans = ""',
        '"CodeActAgent": partial(',
        '"B": 1',
    ],
    'evaluation/agent_bench/run_infer.py': [
        '"AgentBench-OS",',
        'agent_answer = return_val["agent_answer"]',
        'if event.source == "agent":',
    ],
}

@grader
def grade_checkpoint1():
    """
    Check if double quotes are being used in specific locations in the code.
    """
    try:
        for relative_path, lines_to_check in FILES_TO_CHECK.items():
            file_path = os.path.join(OPENHANDS_REPO_PATH, relative_path)
            if not os.path.exists(file_path):
                return False
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()

            for line_to_check in lines_to_check:
                found = False
                for line in content:
                    if line.strip().startswith(line_to_check):
                        if '"' in line and "'" not in line:
                            found = True
                            break
                if not found:
                    return False
        return True
    except Exception as e:
        logging.error(f"Error occurred while checking for double quotes: {e}")
        return False

@grader
def grade_checkpoint2():
    """
    Verify that the existing code is not broken by running the unit tests.
    """
    try: 
        # Change directory to /workspace/openhands
        os.chdir(OPENHANDS_REPO_PATH)
        subprocess.run(['pip', 'install', 'poetry'], check=True)
        # Install dependencies
        subprocess.run(['poetry', 'install'], check=True)
        # checkout to the main branch for tests in case any tests were deleted
        subprocess.run(['git', 'checkout', 'main', '--', 'tests'], check=True)
        # Run unit tests
        result = subprocess.run(['poetry', 'run', 'pytest', './tests/unit/', '--ignore=tests/unit/test_runtime_build.py', '--ignore=tests/unit/test_security.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error occurred while running unit tests: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: Double quotes are being used in specific locations
    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    # Checkpoint 2: Existing code not broken
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    return result
