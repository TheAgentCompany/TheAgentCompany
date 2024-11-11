from typing import List
from scoring import Result, Checkpoint
import subprocess
from common import check_repo_exists, checkpoint

PYPROJECT_TOML_TREE_SITTER_VERSION = """tree-sitter = "0.23.2\""""
PYPROJECT_TOML_ZOPE_INTERFACE_VERSION = """zope-interface = "7.1.1\""""
POETRY_LOCK_TREE_SITTER_VERSION = """name = "tree-sitter"
version = "0.23.2"
"""
POETRY_LOCK_ZOPE_INTERFACE_VERSION = """name = "zope-interface"
version = "7.1.1"
"""

def get_package_version(package_name):
    try:
        # Execute poetry show requests command in the openhands directory
        result = subprocess.run(['poetry', 'show', package_name], 
                              capture_output=True, 
                              text=True,
                              cwd="/workspace/openhands")
        
        # Split the output into lines and look for the version
        lines = result.stdout.split('\n')
        for line in lines:
            if 'version' in line:
                # Extract version number using string splitting
                version = line.split(':')[1].strip()
                return version
                
        return ""
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return ""

@checkpoint
def grade_checkpoint1(trajectory):
    return "root/doc/-/wikis" in trajectory

@checkpoint
def grade_checkpoint2():
    return check_repo_exists("openhands")

@checkpoint
def grade_checkpoint3():
    with open("/workspace/openhands/pyproject.toml") as f:
        code_content = f.read()
        if (
            PYPROJECT_TOML_ZOPE_INTERFACE_VERSION in code_content
            and PYPROJECT_TOML_TREE_SITTER_VERSION in code_content
        ):
            return True
    return False

@checkpoint
def grade_checkpoint4():
    with open("/workspace/openhands/poetry.lock") as f:
        code_content = f.read()
        if (
            POETRY_LOCK_TREE_SITTER_VERSION in code_content
            and POETRY_LOCK_ZOPE_INTERFACE_VERSION in code_content
        ):
            return True
    return False

@checkpoint
def grade_checkpoint5():
    return get_package_version("tree-sitter") == "0.23.2" and get_package_version("zope-interface") == "7.1.1"

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = passed2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    passed4 = passed3 and grade_checkpoint4()
    checkpoints.append(Checkpoint(1, int(passed4)))

    passed5 = passed4 and grade_checkpoint5()
    checkpoints.append(Checkpoint(1, int(passed5)))

    return result

