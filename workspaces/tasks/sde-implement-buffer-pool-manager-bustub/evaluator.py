from typing import List

from litellm import logging

from scoring import Result, Checkpoint
from common import *
import re

############################# init variable #####################################
PROJECT_NAME = "bustub"
TEST_REPO_PATH = "/workspace/bustub"
############################# helper functions #####################################

def run_command_subprocess(command):
    """
    Execute a bash command using subprocess.run()
    Returns: CompletedProcess instance with return code, stdout, and stderr
    """
    try:
        # Run command and capture output
        result = subprocess.run(
            command,
            shell=True,  # Allows running shell commands
            capture_output=True,  # Capture stdout and stderr
            text=True  # Return strings instead of bytes
        )
        return result
    except subprocess.SubprocessError as e:
        logging.error(f"Error executing command: {e}")
        return None

compilation_command  = f"""
        cd {TEST_REPO_PATH} && \
        mkdir build && \
        cd build && \
        cmake .. && \
        make lru_k_replacer_test -j $(nproc) && \
        make disk_scheduler_test -j $(nproc) && \
        make page_guard_test -j $(nproc) && \
        make buffer_pool_manager_test -j $(nproc)
    """
def test_command(test_name):
    return f"{TEST_REPO_PATH}/build/test/{test_name} --gtest_also_run_disabled_tests"

def single_test_case_passed(test_name):
    result = run_command_subprocess(test_command(test_name))
    if result.returncode != 0:
        logging.error(result.stderr)
        return False
    failed = result.stdout.count("FAILED")
    logging.info(result.stdout)
    if failed > 0:
        logging.warning(f"{failed} tests failed in {test_name}")
        return False
    return True
def score_multiple_test_cases(test_name, test_cases_number):
    result = run_command_subprocess(test_command(test_name))
    logging.info(result.stdout)
    match = re.search(r'\s*(\d+)\s+FAILED\s+TEST', result.stdout)
    if match:
        logging.warning(f"{match.group(1)} tests failed in {test_name}")
        return test_cases_number - int(match.group(1))
    if result.returncode != 0:
        logging.error(result.stderr)
        return 0
    return test_cases_number

############################# grade checkpoints #####################################

@grader
def grade_checkpoint1():
    return check_repo_exists(PROJECT_NAME)

@grader
def grade_checkpoint2():
    return single_test_case_passed("lru_k_replacer_test")

@grader
def grade_checkpoint3():
    return single_test_case_passed("disk_scheduler_test")

@grader
def grade_checkpoint4():
    return score_multiple_test_cases("page_guard_test",2)

@grader
def grade_checkpoint5():
    return score_multiple_test_cases("buffer_pool_manager_test", 7)


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoint_1_passed = grade_checkpoint1()

    checkpoints.append(Checkpoint(1, int(checkpoint_1_passed)))
    if checkpoint_1_passed:
        compile = run_command_subprocess(compilation_command)
        if(compile.returncode!=0):
            logging.error(compile.stderr)
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2() if checkpoint_1_passed else False)))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3() if checkpoint_1_passed else False)))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint4() if checkpoint_1_passed else False)))
    checkpoints.append(Checkpoint(7, int(grade_checkpoint5() if checkpoint_1_passed else False)))

    return result
