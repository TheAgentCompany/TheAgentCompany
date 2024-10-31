import logging
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client
from config import *

############################# Init Variables #####################################
# Create RocketChat instance
rocket = create_rocketchat_client()

def grade_checkpoint1(trajectory):
    required_url_parts = [
        "http://the-agent-company.com/root/openhands/-/issues/",
        "label_name[]=bug",
        "sort=created_date",
        "state=opened"
    ]
    return all(part in trajectory for part in required_url_parts)

def grade_checkpoint2():
    messages = get_message("project-ai")
    if not messages:
        return False
    
    keywords = ['bug', 'issues', 'open']

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if all(keyword in message_text for keyword in keywords):
            return True

    return False

def grade_final_checkpoint():
    messages = get_message("project-ai")
    if not messages:
        return False
    
    issue_numbers = ['4166', '4164', '4157', '4158', '4153', '4131', '4127', '4802', '4042', '4017']
    required_info = ['issue', 'title', 'assigned', 'http']
    
    for msg in messages:
        message_text = msg.get('msg', '').lower()
        issues_present = sum(1 for num in issue_numbers if num in message_text)
        info_present = sum(1 for info in required_info if info in message_text)
        
        if issues_present >= 3 and info_present == len(required_info):
            return 2
        elif issues_present > 0 or info_present > 0:
            return 1
    
    return 0

def get_message(channel):
    response = rocket.channels_info(channel=channel).json()
    if not response.get('success'):
        print(f"Failed to retrieve {channel} channel info.")
        return None

    room_id = response['channel']['_id']

    response = rocket.channels_history(room_id=room_id).json()
    if not response.get('success'):
        print("Failed to retrieve message history.")
        return None

    messages = response.get('messages', [])

    if not messages:
        print("No messages found.")
        return None

    return messages
    
def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Accessed OpenHands GitLab repo with correct filters
    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(total=1, result=int(passed1)))

    # Checkpoint 2: Summary message posted in RocketChat #project-ai channel
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(total=1, result=int(passed2)))

    # Final checkpoint: Detailed message posted in RocketChat #project-ai channel
    final_result = grade_final_checkpoint()
    checkpoints.append(Checkpoint(total=1, result=int(final_result)))

    return result