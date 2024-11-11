import shutil
import subprocess
import logging

from typing import List

from scoring import Result, Checkpoint
from common import grader

# Check if go is installed (go version returns "go version xxx")
@grader
def grade_checkpoint1():
    try:
        output = run_command(["go", "version"])
        return output is not None and output.startswith("go version")
    except Exception as e:
            logging.error(f"Fail to grade checkpoint 1: {e}")

# Check if go 1.17 is installed (1.17 keyword is in it)
@grader
def grade_checkpoint2():
    try:
        output = run_command(["go", "version"])
        return output is not None and "1.17" in output
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 2: {e}")

def run_command(command):
    if not shutil.which(command[0]):
        logging.warning(f"Command '{command[0]}' not found in PATH")
        return None
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            logging.warning(f"Command '{' '.join(command)}' failed with return code {result.returncode}")
            return None
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Error running command '{' '.join(command)}': {e}")
        return None


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed_checkpoint1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, passed_checkpoint1))

    passed_checkpoint2 = passed_checkpoint1 and grade_checkpoint2()
    checkpoints.append(Checkpoint(1, passed_checkpoint2))

    return result


