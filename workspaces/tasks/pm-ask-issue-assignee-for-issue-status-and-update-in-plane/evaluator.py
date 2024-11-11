from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history, get_plane_project_id, get_plane_issue_details, get_plane_state_details, checkpoint

CHECKPOINT_1_POINTS = 2
CHECKPOINT_2_POINTS = 1

rocket = create_rocketchat_client()

PROJECT_NAME = 'RisingWave'
PROJECT_ID = get_plane_project_id(PROJECT_NAME)
ISSUE_NAME = 'Evaluate data throughput'
ASSIGNEE_USERNAME = 'zhang_wei'

@checkpoint
def grade_checkpoint1():
    chat_history = get_rocketchat_personal_chat_history(rocket, ASSIGNEE_USERNAME)
    return chat_history is not None and len(chat_history) > 0

@checkpoint
def grade_checkpoint2():
    issue = get_plane_issue_details(PROJECT_ID, ISSUE_NAME)
    if issue is None:
        return False
    state = get_plane_state_details(PROJECT_ID, issue['state'])
    if state is None:
        return False
    return state['group'] == 'completed'

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = passed1 and grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))

    return result
