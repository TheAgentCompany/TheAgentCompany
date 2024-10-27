import requests
import sys

from common import *
rocket=create_rocketchat_client()

def checkpoint1():
    if len(sys.argv) < 2:
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            return False
    return "http://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/8eba9853-4178-42a6-b113-e66002e8e0ab" in trajectory and "http://the-agent-company.com:8091/tac/projects/73cb74f7-a7ac-4292-a915-e2f59a09a703/issues/5d1c8695-acfd-44c2-8d2d-e41c67cdd8c0" in trajectory

def checkpoint2():
    if len(sys.argv) < 2:
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            return False
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

    issue_1 = get_plane_issue_details(project_id, issue_name_1)
    issue_2 = get_plane_issue_details(project_id, issue_name_2)

    state_map, id_map = get_plane_state_id_dict(project_id)

    state_1 = issue_1.get('state') == state_map['In Progress']
    state_2 = issue_2.get('state') == state_map['Done']

    return bool(state_1) and bool(state_2)


def calculate_total_score():
    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 2,
        checkpoint4: 2,

    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"\ntotal point is: {total}")


