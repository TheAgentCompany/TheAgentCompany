import logging
from typing import List
from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_channel_history, evaluate_with_llm, grader

# Create RocketChat instance
rocket = create_rocketchat_client()

@grader
def grade_checkpoint1(trajectory):
    # Check if the agent visits Task_assignment.xlsx on Nextcloud
    target_url = "Documents/Marketing"
    return target_url in trajectory

@grader
def grade_checkpoint2():
    # Check if the agent creates a channel called "Group2" and is public
    channels = rocket.channels_list().json().get('channels', [])
    return any(channel['name'] == "Group2" for channel in channels)

@grader
def grade_checkpoint3():
    # Check if Li Ming and Emily Zhou are in the channel "Group2"
    channel_info = rocket.channels_members(channel="Group2").json()
    if not channel_info.get('success'):
        logging.warning("Failed to retrieve channel info for 'Group2'.")
        return False

    members = [member['username'] for member in channel_info.get('members', [])]
    return "li_ming" in members and "emily_zhou" in members

@grader
def grade_checkpoint4():
    # Check if the agent sends a message containing "@li_ming" and "add a cover image for each video"
    messages = get_rocketchat_channel_history(rocket, "Group2")
    message_list = list(map(lambda message: message['msg'], messages))
    predicate = "There is a message directed to @li_ming that instructs them to add a cover image for each music video"
    return evaluate_with_llm("\n".join(message_list), predicate)

@grader
def grade_checkpoint5():
    # Check if the agent sends a message containing "@emily_zhou" and "write a description for each video"
    messages = get_rocketchat_channel_history(rocket, "Group2")
    message_list = list(map(lambda message: message['msg'], messages))
    predicate = "There is a message directed to @emily_zhou that instructs her to write a description for each video"
    return evaluate_with_llm("\n".join(message_list), predicate)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint5())))
    return result
