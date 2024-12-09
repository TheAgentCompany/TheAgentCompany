import os
import ast
import sys
import logging
import subprocess
import time
import re
import astor


from typing import List
from scoring import Result, Checkpoint
from common import *

REPO_DIR = '/workspace/openhands/'
UT_FILE = REPO_DIR + 'tests/unit/test_agent_skill.py'
COV_FILE = REPO_DIR + 'tests/unit/test_agent_skill_coverage.xml'

def config_env(dir_path):
    """configure enviroment"""
    try:
        os.chdir(dir_path)

        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
    except Exception as e:
        logging.warning(f"is_test_run configure step 1. {e}")
        subprocess.run([sys.executable, "-m", "pip", "install", "poetry"], check=True)
        time.sleep(5)

    logging.info(f"Installing dependencies...")
    try:
        result = subprocess.run(["poetry", "install"], capture_output=True, text=True)
    except Exception as e:
        logging.warning(f"is_test_run configure step 2. {e}")
        return False

    if result.returncode != 0:
        logging.warning(f"Error installing dependencies. {e}")
        logging.warning(f"{result.stderr}")
        return False
    else:
        logging.info(f"Dependencies installed successfully.")

def check_with_llm(test_code, func_code):
    test_content = test_code
    func_content = func_code

    if len(test_content) == 0:
        return False
    if len(func_content) == 0:
        return False

    messages = [
        {
            "content": f"Does the function named 'test_scroll_down' in the text '{test_content}' thoroughly and meaningfully test the 'scroll_down' functionality? The test should include specific assertions that validate the expected behavior of the function '{func_content}', and must not contain trivial or non-functional code such as 'return True' or 'assert 1 == 1'. Does it properly verify the output, state changes, or side effects that should occur when 'scroll_down' is executed? Answer 'yes' if it does, or 'no' if it doesn't. Don't answer anything else.",
            "role": "user"}
    ]
    llm_resonse = llm_complete(messages)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        return True
    else:
        return False

def is_file_exist(file_path):
    """
     Check if a file exists at the given path.
    """
    if not file_path:
        logging.warning("is_file_exist: Empty path provided")
        return False

    abs_path = os.path.abspath(file_path)

    try:
        return os.path.isfile(abs_path)
    except Exception as e:
        logging.warning(f"Error in is_file_exist: {e}")
        return False

def is_function_exists(file_path, function_name):
    """
    Check if a specific function exists in a Python file.
    """
    try:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return True

        return False

    except Exception as e:
        logging.warning(f"Error parsing file {file_path}: {e}")
        return False

def get_function_content(file_path, function_name):
    """
    get a specific function's code.
    """
    try:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return astor.to_source(node)

        return None
    except Exception as e:
        logging.warning(f"Error parsing file {file_path}: {e}")
        return False

def is_test_run(dir_path, file_path, function_name):
    """
    Run a specific test function using pytest and check if it was successful.
    """
    # run test
    try:
        command = [sys.executable, "-m", "pytest", f"{file_path}::{function_name}", "-v"]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0 and f"{function_name} PASSED" in result.stdout:
            return True
        else:
            logging.warning(f"{result.stdout}")
            logging.warning(f"is_test_run: {result.stderr}")
            return False

    except Exception as e:
        logging.warning(f"An error occurred while running the test: {e}")
        return False

def run_pytest_with_stats(cov_file_path, ut_file_path, function_name=''):
    """
    Run pytest and collect test statistics.
    """
    try:
        if function_name:
            command = f"poetry run pytest --forked --cov=openhands --cov-report=xml:{cov_file_path} -svv {ut_file_path}::{function_name}"
        else:
            command = f"poetry run pytest --forked --cov=openhands --cov-report=xml:{cov_file_path} -svv {ut_file_path}"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Parse test statistics
        output = result.stdout
        stats = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }

        # Use regex to match results
        patterns = {
            'passed': r'(\d+) passed',
            'failed': r'(\d+) failed',
            'skipped': r'(\d+) skipped'
        }

        # Extract numbers for each test result type
        for key, pattern in patterns.items():
            match = re.search(pattern, output)
            if match:
                stats[key] = int(match.group(1))

        # Calculate total tests
        stats['total'] = stats['passed'] + stats['failed'] + stats['skipped']

    except Exception as e:
        logging.warning(f"Error in run_pytest_with_stats: {e}")
        return False

    return stats

@grader
def grade_checkpoint1():
    return check_repo_exists('openhands')

@grader
def grade_checkpoint2(path='/workspace/openhands/tests/unit/test_agent_skill.py', function_name='test_scroll_down'):
    return is_function_exists(file_path=path, function_name=function_name)

@grader
def grade_checkpoint3(cov_file_path=COV_FILE, ut_file_path=UT_FILE, function_name='test_scroll_down'):
    status = run_pytest_with_stats(cov_file_path=cov_file_path, ut_file_path=ut_file_path, function_name=function_name)
    if not status:
        return False

    return True if status['passed']==1 else False

@grader
def grade_checkpoint4():
    test_content = get_function_content(file_path='/workspaces/openhands/tests/unit/test_agent_skill.py', function_name='test_scroll_down')
    func_content = get_function_content(file_path='/workspaces/openhands/openhands/runtime/plugins/agent_skills/file_ops/file_ops.py', function_name='scroll_down')

    if not test_content:
        return False
    if not func_content:
        return False

    return check_with_llm(
        test_code=test_content,
        func_code=func_content,
    )


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Define the scores corresponding to when each function is True
    scores = {
        grade_checkpoint1: 1,
        grade_checkpoint2: 1,
        grade_checkpoint3: 2,
        grade_checkpoint4: 1
    }

    for func, total_score in scores.items():
        checkpoints.append(Checkpoint(total_score, total_score * int(func())))

    return result



