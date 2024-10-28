import json
import logging
from scoring import Result, Checkpoint
from common import *
from typing import List

from sqlalchemy import false


def get_plane_all_issue_state(projects):
    state_count= {}
    try:
        for project in projects:
            state_map, id_map = get_plane_state_id_dict(project_id=project['id'])
            state_count[project.get('name')]={}
            for key in state_map.keys():
                state_count[project.get('name')][key] = 0
            issues = get_plane_project_all_issues(project.get('id'))
            for issue in issues:
                state_count[project.get('name')][id_map[issue['state']] ] += 1
        return state_count
    except Exception as e:
        logging.warning(f"Get all issues state failed: {e}")
        return {}

def checkpoint1():
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

def checkpoint2(filepath):
    projects = get_all_plane_projects()
    state_count_cur = get_plane_all_issue_state(projects)

    try:
        with open(filepath, 'r') as f:
            state_count_old = json.load(f)
        active_counts_old = {}
        for project, statuses in state_count_old.items():
            for key, value in statuses.items():
                if key in ['Backlog', 'Todo', 'In Progress'] and value > 0:
                    statuses[key] -= value
                    statuses['Done'] += value
            active_counts_old[project] = statuses
    except Exception as e:
        logging.warning(f"checkpoint2 failed: {e}")
        return False

    return state_count_cur==active_counts_old

def grade_checkpoints(trajectory=''):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = checkpoint2(filepath='result.json')
    checkpoints.append(Checkpoint(2, 2 * int(passed2)))

    return result

if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))


