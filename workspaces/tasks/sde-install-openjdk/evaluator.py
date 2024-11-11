import shutil
import subprocess
import logging
from typing import List


from scoring import Result, Checkpoint
from common import grader

# OpenJDK is installed
@grader
def grade_checkpoint1():
    try:
        output = run_command(["java", "--version"])
        return output is not None and "openjdk" in output.lower()
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 1: {e}")
        return False

# OpenJDK 17 is installed
@grader
def grade_checkpoint2():
    try:
        output = run_command(["java", "--version"])
        return output is not None and "openjdk 17." in output.lower()
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 2: {e}")
        return False

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


