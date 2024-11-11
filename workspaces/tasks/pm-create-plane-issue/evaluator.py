from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from config import *
from common import get_plane_project_id, get_plane_project_all_issues, checkpoint

# Constants
PROJECT_NAME = "Frontend Development"
ISSUE_TITLE = "Improve Page Loading Speed"
EXPECTED_PROJECT_TRAJECTORY = "http://the-agent-company.com:8091/tac/projects/39ccbb74-8f1d-4259-8f75-df9ffbc9a962/issues/"


@checkpoint
def grade_checkpoint1(trajectory: str):
    """
    Check if the agent accessed the correct project page by verifying the project ID and trajectory.
    """
    # Check if the trajectory contains the expected project URL
    return EXPECTED_PROJECT_TRAJECTORY in trajectory

@checkpoint
def grade_checkpoint2():
    """
    Check if the issue "Improve Page Loading Speed" is created in the correct project.
    """
    project_id = get_plane_project_id(PROJECT_NAME)
    if not project_id:
        return False  # Project does not exist
    
    issues = get_plane_project_all_issues(project_id)
    return any(issue.get("name", "").strip().lower() == ISSUE_TITLE.lower() for issue in issues)

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Accessed the correct project page
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Issue "Improve Page Loading Speed" is created
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    return result


