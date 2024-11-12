from typing import List
from scoring import Result, Checkpoint
import subprocess
import os
from common import grader

def check_workflow_files() -> bool:
    """Check if specific GitHub workflow files have been updated to use UV."""
    try:
        workflow_files = {
            "mypy.yml": "uv run mypy --strict .",
            "publish-to-pypi.yml": "uv publish",
        }
        workflow_dir = "/workspace/sotopia/.github/workflows"
        for file, uv_command in workflow_files.items():
            file_path = os.path.join(workflow_dir, file)
            if os.path.exists(file_path):
                with open(file_path) as f:
                    content = f.read().lower()
                    if 'poetry' in content:
                        return False
                    if uv_command not in content:
                        return False
            else:
                return False
        return True
    except Exception:
        return False

def check_documentation_files() -> bool:
    """Check if documentation has been updated for UV."""
    try:
        docs = [
            "/workspace/sotopia/docs/pages/contribution/contribution.md",
            "/workspace/sotopia/docs/pages/examples/examples.mdx",
            "/workspace/sotopia/docs/pages/index.mdx"
        ]
        for doc in docs:
            with open(doc) as f:
                content = f.read().lower()
                if 'poetry' in content:
                    return False
                if 'uv' not in content:
                    return False
        return True
    except Exception:
        return False
    
def check_pyproject_toml() -> bool:
    """Check if pyproject.toml has been updated to use UV."""
    try:
        with open('/workspace/sotopia/pyproject.toml') as f:
            content = f.read()
            if 'poetry' in content:
                return False
            if 'uv' not in content:
                return False
        result = subprocess.run(['uv', 'sync', '--all-extras'], cwd='/workspace/sotopia', capture_output=True, text=True)
        if result.returncode != 0:
            return False
        return True
    except Exception:
        return False

@grader
def grade_checkpoint1() -> bool:
    """Grade GitHub workflow updates."""
    return check_workflow_files()

@grader
def grade_checkpoint2() -> bool:
    """Grade documentation updates."""
    return check_documentation_files()

@grader
def grade_checkpoint3() -> bool:
    """Grade pyproject.toml updates."""
    return check_pyproject_toml()

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(2, int(passed1) * 2))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(3, int(passed2) * 3))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(3, int(passed3) * 3))

    return result
