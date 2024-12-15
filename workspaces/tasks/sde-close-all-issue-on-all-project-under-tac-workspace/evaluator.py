import json
import logging
from scoring import Result, Checkpoint
from common import *
from typing import List
from helper import get_plane_all_issue_state


@grader
def grade_checkpoint1():
    projects = get_all_plane_projects()
    state_count = get_plane_all_issue_state(projects)
    active_counts = {}
    for project, statuses in state_count.items():
        active_count = sum(
            count for status, count in statuses.items()
            if status not in ['Done', 'Cancelled']
        )
        active_counts[project] = active_count
    result = 0
    for active_count in active_counts.values():
        result += active_count
    return not bool(result)

@grader
def grade_checkpoint2(filepath):
    projects = get_all_plane_projects()
    new_state = get_plane_all_issue_state(projects)
    if not new_state:
        return False      
    try:
        with open(filepath, 'r') as f:
            old_state = json.load(f)
        for project, statuses in old_state.items():
            closed_count = sum(value for key, value in statuses.items() if key in ['Backlog', 'Todo', 'In Progress']) + statuses.get('Done', 0)
            cancelled_count = statuses.get('Cancelled', 0)
            if new_state[project]['Cancelled'] != cancelled_count:
                return False
            if new_state[project]['Done'] != closed_count:
                return False
    except Exception as e:
        logging.warning(f"checkpoint2 failed: {e}")
        return False
    return True

def grade_checkpoints(trajectory=''):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    # NOTE: The result.json is generated in pre_init.py
    passed2 = grade_checkpoint2(filepath='result.json')
    checkpoints.append(Checkpoint(2, 2 * int(passed2)))

    return result

if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))

