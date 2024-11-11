import logging
import subprocess

from typing import List

from scoring import Result, Checkpoint
from common import *

@checkpoint
def grade_checkpoint1():
    try:
        result = subprocess.run(['git', '-C', '/workspace/sotopia', 'branch', '--list', 'feature/update-ci'], capture_output=True, text=True)
        if 'feature/update-ci' in result.stdout:
            logging.info("Branch 'feature/update-ci' exists in the local repository.")
            return True
        else:
            logging.warning("Branch 'feature/update-ci' does not exist in the local repository.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the local repository: {e}")
        return False

@checkpoint
def grade_checkpoint2():
    try:
        with open('/workspace/sotopia/.github/workflows/cli_tests.yml', 'r') as file:
            content = file.read()
            if 'macos-latest' in content:
                logging.info("macOS version is updated to 'macos-latest' in cli_tests.yml.")
                return True
            else:
                logging.warning("macOS version is not updated to 'macos-latest' in cli_tests.yml.")
                return False
    except FileNotFoundError:
        logging.error("File cli_tests.yml not found.")
        return False
    except Exception as e:
        logging.error(f"Error occurred while checking cli_tests.yml: {e}")
        return False

@checkpoint
def grade_checkpoint3():
    try:
        with open('/workspace/sotopia/.github/workflows/cli_tests.yml', 'r') as file:
            content = file.read()
            if 'amd64' in content and 'x86' in content:
                logging.info("CI for amd and x86 is added in cli_tests.yml.")
                predicate = "CI for amd and x86 is added"
                llm_result = evaluate_with_llm(content, predicate)
                return llm_result
            else:
                logging.warning("CI for amd and x86 is not added in cli_tests.yml.")
                return False
    except FileNotFoundError:
        logging.error("File cli_tests.yml not found.")
        return False
    except Exception as e:
        logging.error(f"Error occurred while checking cli_tests.yml: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: create branch
    passed_checkpoint1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint1)))

    # Checkpoint 2: Update macOS version
    passed_checkpoint2 = passed_checkpoint1 and grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint2)))

    # Checkpoint 3: Add CI for amd and x86
    passed_checkpoint3 = passed_checkpoint2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint3)))

    return result



