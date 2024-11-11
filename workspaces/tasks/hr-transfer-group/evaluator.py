
import logging
from typing import List

from scoring import Result, Checkpoint

from common import evaluate_with_llm
from common import create_rocketchat_client, grader

# Create RocketChat instance
rocket = create_rocketchat_client()
############################# Helper Functions #####################################

def get_channel_room_id(channel_name):
    """Get the room_id for a specific channel by its name."""
    response = rocket.channels_info(channel=channel_name).json()
    if response.get('success'):
        return response['channel']['_id']
    return None

@grader
def check_if_user_in_channel(channel_name: str, username: str):
    room_id = get_channel_room_id(channel_name)
    if not room_id:
        print(f"Failed to find room ID for channel #{channel_name}.")
        return None
    members = rocket.channels_members(channel=channel_name).json()
    users_list = members.get("members")
    return any(user['name'] == username for user in users_list)

@grader
def check_job_description(username: str):

    user_info = rocket.users_info(username=username).json().get('user', {})
    job_description = user_info.get('bio', '')
    print(f"{username}''s Job Description: {job_description}")

    predicate = 'the person does not work in database team and now works in the AI team'
    return evaluate_with_llm(job_description, predicate)

############################# Evaluator #####################################

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    employee = "Li Ming"
    user_name = "li_ming"

    res =  check_if_user_in_channel("project-graphdb", employee)
    if res is not None and not res:
        logging.info("succesfully removed from #project-graphdb channel")
        checkpoints.append(Checkpoint(1, 1))
    else:
        checkpoints.append(Checkpoint(1, 0))
    
    res = check_if_user_in_channel("project-ai", employee)
    if res:
        logging.info("succesfully added to #project-ai channel")
        checkpoints.append(Checkpoint(1, 1))
    else:
        checkpoints.append(Checkpoint(1, 0))

    if check_job_description(user_name):
        logging.info("Job description succesfully updated")
        checkpoints.append(Checkpoint(1, 1))
    else:
        checkpoints.append(Checkpoint(1, 0))

    return result


