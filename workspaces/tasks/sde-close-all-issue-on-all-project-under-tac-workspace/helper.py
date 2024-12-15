import logging
from common import *

def get_plane_all_issue_state(projects):
    """
    Returns a nested dictionary containing issue state counts for each project
    Return structure:
    {
        'JanusGraph': {
            'Backlog': 0,
            'Todo': 0,
            'In Progress': 2,
            'Done': 4,
            'Cancelled': 0
        },
        'RisingWave': {
            'Backlog': 0,
            'Todo': 0,
            'In Progress': 0,
            'Done': 6,
            'Cancelled': 0
        },
    }
    """
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
