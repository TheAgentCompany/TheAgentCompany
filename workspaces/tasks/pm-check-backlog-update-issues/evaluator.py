import requests
import logging
import os
from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, get_plane_project_id, get_plane_state_id_dict, get_plane_project_all_issues, check_rocketchat_message_posted, grader
from config import *

# Create RocketChat instance
rocket = create_rocketchat_client()


@grader
def grade_checkpoint1(trajectory):
    """Check if part of the project URL is accessed in the trajectory."""
    target_substring = "/tac/projects/a063d05f-37cf-4f97-b10c-486acf13b138/issues/"
    return target_substring in trajectory


@grader
def grade_checkpoint2():
    """Check if a message was posted in Rocket.Chat identifying the specific issue 'NODER-3' with correct details."""

    keywords = ["noder-3", "enhance error handling mechanism in node-red flows", "liu_qiang"]
    
    # Reuse check_message_posted with the defined keywords
    return check_rocketchat_message_posted(rocket, "project-lowcode", keywords)

@grader
def grade_checkpoint3():
    """Check if a follow-up message confirming updates to Plane was already posted in Rocket.Chat."""
    follow_up_message = ["Okay I will update Plane to reflect this"]
    return check_rocketchat_message_posted(rocket, "project-lowcode", follow_up_message)

def grade_final_checkpoint():
    """Check if the issue 'Enhance Error Handling Mechanism in Node-RED Flows' in the 'Node-RED' project has a status of 'Done'."""
    
    # Define the specific project and issue name
    project_name = "Node-RED"
    issue_name = "Enhance Error Handling Mechanism in Node-RED Flows"
    
    # Get the project ID for 'Node-RED'
    project_id = get_plane_project_id(project_name)
    if not project_id:
        logging.warning(f"Project '{project_name}' not found.")
        return False
    
    # Get state mappings (state_map has readable state names mapped to IDs)
    state_map, id_map = get_plane_state_id_dict(project_id)
    
    # Normalize case of state names for case-insensitive matching
    state_map = {name.lower(): id for name, id in state_map.items()}
    
    # Check for "done" status (case-insensitive)
    done_status_id = state_map.get("done")
    if not done_status_id:
        logging.warning("The 'Done' status ID was not found in state mappings.")
        return False
    
    # Retrieve issues for the project
    issues = get_plane_project_all_issues(project_id)
    
    # Look for the specified issue name and check if its state is "Done"
    for issue in issues:
        if issue.get("name") == issue_name and issue.get("state") == done_status_id:
            return True
    
    # Return False if the specific issue is not found or is not marked as "Done"
    return False


############################# Evaluator #####################################

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Access Node-RED project
    passed1 = grade_checkpoint1("http://the-agent-comapny.com/tac/projects/a063d05f-37cf-4f97-b10c-486acf13b138/issues/")
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Identify and post blocked/backlog issues in Rocket.Chat
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(2, 2 * int(passed2)))

    # Checkpoint 3: Confirm follow-up
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    # Final Checkpoint: Update issue statuses to "Done"
    passed_final = grade_final_checkpoint()
    checkpoints.append(Checkpoint(1, int(passed_final)))

    return result


