import json
from pathlib import Path
import logging
from common import *
from helper import get_plane_all_issue_state

def write_json(data, filepath):
    try:
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logging.warning(f"Write json failed: {str(e)}")
        return False

if __name__ == "__main__":
    projects = get_all_plane_projects()
    state_count = get_plane_all_issue_state(projects)
    write_json(state_count, "result.json")




