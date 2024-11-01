from typing import List
from scoring import Result, Checkpoint
import subprocess
import os

def check_workflow_files() -> bool:
    """Check if GitHub workflow files have been updated to use UV."""
    try:
        workflow_dir = "/workspace/sotopia/.github/workflows"
        for file in os.listdir(workflow_dir):
            if file.endswith('.yml') or file.endswith('.yaml'):
                with open(os.path.join(workflow_dir, file)) as f:
                    content = f.read()
                    if 'poetry' in content:
                        return False
                    if 'uv' not in content.lower():
                        return False
        return True
    except Exception:
        return False

def check_documentation_files() -> bool:
    """Check if documentation has been updated for UV."""
    try:
        docs = [
            "/workspace/sotopia/contribution.md",
            "/workspace/sotopia/examples.mdx",
            "/workspace/sotopia/index.mdx"
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

def grade_checkpoint1() -> bool:
    """Grade GitHub workflow updates."""
    return check_workflow_files()

def grade_checkpoint2() -> bool:
    """Grade documentation updates."""
    return check_documentation_files()

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(3, int(passed1) * 3))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(3, int(passed2) * 3))

    return result