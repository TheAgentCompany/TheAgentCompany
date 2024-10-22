import os
import ast
import sys
import logging
import subprocess
import time
import xml.etree.ElementTree as ET
import astor
import re

REPO_DIR = '/workspace/openhands/'
UT_FILE = '/Users/bytedance/code_ex/TheAgentCompany/workspaces/OpenHands/tests/unit/test_agent_skill.py' #'/workspace/openhands/tests/unit/test_agent_skill.py'
COV_FILE = '/workspace/openhands/tests/unit/test_agent_skill_coverage.xml'

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

def is_dir(fir_path):
    """
    Check if the given path is a directory and contains at least one file.
    """
    if not fir_path:
        logging.warning("is_dir: Empty path provided")
        return False
    try:
        abs_path = os.path.abspath(fir_path)

        if not os.path.exists(abs_path):
            logging.warning(f"is_dir: Path does not exist: {abs_path}")
            return False

        if not os.path.isdir(abs_path):
            logging.warning(f"is_dir: Path is not a directory: {abs_path}")
            return False

        files = os.listdir(abs_path)

        if not files:
            logging.warning(f"is_dir: No files found in directory: {abs_path}")
            return False

        return True

    except Exception as e:
        logging.warning(f"Error in is_dir: {e}")
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

def is_repo_exit(dir_path):
    """
     Check if a repo exists at the given path.
    """
    is_dir(dir_path)

    instruction_file_name = ".openhands_instructions"
    instruction_file_path = os.path.join(dir_path, instruction_file_name)

    return is_file_exist(instruction_file_path)

def is_test_run(file_path, function_name):
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

def run_pytest_with_stats(cov_file_path, ut_file_path):
    """
    Run pytest and collect test statistics.
    """
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

    return stats

def get_line_cov_rate(cov_file_path=COV_FILE):
    """
    Extract coverage information for file_ops.py from coverage XML report.
    """
    # Parse XML file
    try:
        tree = ET.parse(cov_file_path)
        root = tree.getroot()

        # Find the specific class element
        for class_elem in root.findall('.//class'):
            if class_elem.get('name') == 'file_ops.py':
                return float(class_elem.get('line-rate'))
        return None
    except Exception as e:
        logging.warning(f"Error in get_line_cov_rate: {e}")
        return False

def remove_func(file_path=UT_FILE):
    """
    Remove test_append_file function from the specified test file.
    """
    try:
        # Read all lines from file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Find function boundaries
        start_idx = None
        end_idx = None

        for i, line in enumerate(lines):
            # Look for function definition
            if line.strip().startswith('def test_append_file('):
                start_idx = i
                # Find the end of function (first non-indented line after start)
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(' '):
                        end_idx = j
                        break
                if end_idx is None:  # If function extends to end of file
                    end_idx = len(lines)
                break

        if start_idx is not None:
            # Remove the function
            del lines[start_idx:end_idx]

            # Write back to file
            with open(file_path, 'w') as file:
                file.writelines(lines)

            print(f"Successfully removed test_append_file function")
            return True

        print("Function test_append_file not found in file")
        return False

    except Exception as e:
        print(f"Error: File not found at {file_path}")
        return False

def checkpoint1(path=REPO_DIR):
    return is_repo_exit(dir_path=path)

def checkpoint2(path=UT_FILE):
    return is_file_exist(file_path=path)

def checkpoint3(path=UT_FILE, function_name='test_append_file'):
    return is_function_exists(file_path=path, function_name=function_name)

def checkpoint4(path=UT_FILE, function_name='test_append_file'):
    return is_test_run(file_path=path, function_name=function_name)

def checkpoint5(cov_file_path=COV_FILE, ut_file_path=UT_FILE):
    before_stats = run_pytest_with_stats(cov_file_path=cov_file_path, ut_file_path=ut_file_path)

    before_cov_rate = get_line_cov_rate(cov_file_path)
    if not before_cov_rate:
        return False

    test_function = '''
    def test_append_file(tmp_path):
        temp_file_path = tmp_path / 'a.txt'
        content = 'Line 1\\nLine 2'
        temp_file_path.write_text(content)

        open_file(str(temp_file_path))

        with io.StringIO() as buf:
            with contextlib.redirect_stdout(buf):
                append_file(str(temp_file_path), content='APPENDED TEXT')
            result = buf.getvalue()
            expected = (
                f'[File: {temp_file_path} (3 lines total after edit)]\\n'
                '(this is the beginning of the file)\\n'
                '1|Line 1\\n'
                '2|Line 2\\n'
                '3|APPENDED TEXT\\n'
                '(this is the end of the file)\\n'
                + MSG_FILE_UPDATED.format(line_number=2)
                + '\\n'
            )
            assert result.split('\\n') == expected.split('\\n')

        with open(temp_file_path, 'r') as file:
            lines = file.readlines()
        assert len(lines) == 3
        assert lines[0].rstrip() == 'Line 1'
        assert lines[1].rstrip() == 'Line 2'
        assert lines[2].rstrip() == 'APPENDED TEXT'
    '''
    with open(ut_file_path, 'a') as file:
        file.write(test_function)

    after_stats = run_pytest_with_stats(cov_file_path=cov_file_path, ut_file_path=ut_file_path)

    before_stats['passed'] = before_stats['passed']+1
    if after_stats != before_stats:
        return False

    after_cov_rate = get_line_cov_rate(cov_file_path)
    if not after_cov_rate:
        return False

    return True if after_cov_rate>before_cov_rate else False

def calculate_total_score():
    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
        checkpoint4: 2,
        checkpoint5: 1
    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score


# compute the total point
# total = calculate_total_score()
# print(f"\ntotal point is: {total}")

remove_func()
