import json
import sys
from scoring import Result, Checkpoint
from common import *
from typing import List

from sqlalchemy.testing.plugin.plugin_base import logging

rocket=create_rocketchat_client()

def checkpoint1(trajectory):
    return "http://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/8eba9853-4178-42a6-b113-e66002e8e0ab" in trajectory and "http://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/5d1c8695-acfd-44c2-8d2d-e41c67cdd8c0" in trajectory

def checkpoint2(trajectory):
    return "http://the-agent-company.com:3000/home" in trajectory

def checkpoint3():
    msgs_1 = get_chat_history(rocket, username='mike_chen')
    msgs_2 = get_chat_history(rocket, username='wang_fang')
    return bool(msgs_1) and bool(msgs_2)

def checkpoint4():
    project_name = "OpenHands"
    issue_name_1 = "Model: recall rate is 0"
    issue_name_2 = "Model: security problem"

    project_id = get_plane_project_id(project_name)

    if not project_id:
        return False

    issue_1 = get_plane_issue_details(project_id, issue_name_1)
    issue_2 = get_plane_issue_details(project_id, issue_name_2)

    if not issue_1 or not issue_2:
        return False

    state_map, id_map = get_plane_state_id_dict(project_id)

    if not state_map or not id_map:
        return False

    try:
        state_1 = issue_1.get('state') == state_map['In Progress']
        state_2 = issue_2.get('state') == state_map['Done']
    except Exception as e:
        logging.warning("Error in get state", e)
        return False

    return bool(state_1) and bool(state_2)


def grade_checkpoints(trajectory='http://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/8eba9853-4178-42a6-b113-e66002e8e0ab\nhttp://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/5d1c8695-acfd-44c2-8d2d-e41c67cdd8c0\nhttp://the-agent-company.com:3000/home'):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    passed4 = checkpoint4()
    checkpoints.append(Checkpoint(2, 2 * int(passed4)))
    return result

if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))


