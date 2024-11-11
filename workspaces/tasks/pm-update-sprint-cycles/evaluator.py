import requests
from datetime import datetime, timezone
import logging

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from config import PLANE_BASEURL,PLANE_WORKSPACE_SLUG,PLANE_HEADERS
from common import create_rocketchat_client, get_plane_project_id, get_plane_issues_by_project_cycle, checkpoint
# Create RocketChat instance
rocket = create_rocketchat_client()


def get_rocketchat_channel_room_id(rocket_client, channel_name):
    """Get the room_id for a specific channel."""
    response = rocket_client.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

def check_rocketchat_message_posted_keyword_set(rocket_client, channel_name, keyword_sets):
    """
    Check if messages containing specific keywords were posted in the specified channel.
    Args:
        rocket_client: An instance of the RocketChat client.
        channel_name (str): Name of the Rocket.Chat channel.
        keyword_sets (list of list): List of lists, where each sublist contains keywords for a specific message to check.
    Returns:
        bool: True if messages satisfying each keyword set are found, False otherwise.
    """
    room_id = get_rocketchat_channel_room_id(rocket_client, channel_name)
    if not room_id:
        return False

    # Fetch recent messages
    messages = rocket_client.channels_history(room_id=room_id, count=10).json().get('messages', [])
    message_texts = [message.get("msg", "").lower() for message in messages]

    # Check each set of keywords independently
    for keywords in keyword_sets:
        # Find a message that contains all keywords in the current set
        if not any(all(keyword.lower() in message_text for keyword in keywords) for message_text in message_texts):
            return False  # If no message contains all keywords in the current set, return False
    
    return True  # All keyword sets were found in some message


@checkpoint
def grade_checkpoint1(trajectory):
    """Check if the evaluator accessed 'RisingWave' project and navigated to 'Cycles'."""
    # This check can be simulated by a keyword in the trajectory, e.g., accessing "Cycles" section
    return "RisingWave" in trajectory and "Cycles" in trajectory


def get_cycle_id_by_name(project_id, cycle_name="Sprint 1"):
    """Retrieve the ID of a specific cycle by name for the given project."""
    url = f"{PLANE_BASEURL}/api/v1/workspaces/{PLANE_WORKSPACE_SLUG}/projects/{project_id}/cycles"
    try:
        response = requests.get(url, headers=PLANE_HEADERS)
        response.raise_for_status()
        cycles = response.json().get('results', [])
        
        # Find the cycle with the specified name
        for cycle in cycles:
            if cycle.get("name") == cycle_name:
                return cycle.get("id")
        
        logging.warning(f"Cycle '{cycle_name}' not found.")
    except Exception as e:
        logging.warning(f"Failed to retrieve cycles: {e}")
    
    return None


@checkpoint
def grade_checkpoint2():
    """Check if specific issues are present in the 'Sprint 2' cycle."""
    
    # Define project and issue names to check
    project_name = "RisingWave"
    required_issue_names = {
        "Identify necessary operators and requirements",
        "Conduct memory usage analysis"
    }
    
    # Get project ID
    project_id = get_plane_project_id(project_name)
    if not project_id:
        logging.warning(f"Project '{project_name}' not found.")
        return False
    
    # Get the ID of "Sprint 2"
    sprint_2_cycle_id = get_cycle_id_by_name(project_id, "Sprint 2")
    if not sprint_2_cycle_id:
        logging.warning("Sprint 2 cycle ID not found.")
        return False
    
    # Get all issues in the "Sprint 2" cycle
    issues_in_sprint_2 = get_plane_issues_by_project_cycle(project_id, sprint_2_cycle_id)
    
    # Collect names of issues in "Sprint 2"
    issue_names_in_sprint_2 = {issue.get("name") for issue in issues_in_sprint_2}
    
    # Check if required issues are in "Sprint 2"
    return required_issue_names.issubset(issue_names_in_sprint_2)


@checkpoint
def grade_checkpoint_final():
    """Confirm that notification messages were posted to Rocket.Chat with the specified issue names and assignee name variations."""
    
    # Define specific pairs of issue names and their corresponding assignee name variations
    keywords = [
    ["liu_qiang", "identify necessary operators and requirements"],
    ["zhang_wei", "conduct memory usage analysis"]
    ]

    if not check_rocketchat_message_posted_keyword_set(rocket, "project-streamdb", keywords):
        return False  # If any message is missing, return False
    
    return True  # All required messages are found


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Access 'RisingWave' project and navigate to 'Cycles'
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Identify unfinished issues and move them to the next sprint
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(2, 2 * int(passed2)))

    # Checkpoint 3: Notify assignees on Rocket.Chat
    passed3 = grade_checkpoint_final()
    checkpoints.append(Checkpoint(1, int(passed3)))

    return result




