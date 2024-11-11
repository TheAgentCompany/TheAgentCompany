import logging
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, get_rocketchat_channel_history, checkpoint
from config import *

############################# Init Variables #####################################
# Create RocketChat instance
rocket = create_rocketchat_client()



@checkpoint
def grade_checkpoint1(trajectory):
    required_url_parts = [
        "/root/openhands/-/issues/",
        "label_name[]=bug",
        "state=opened"
    ]
    return all(part in trajectory for part in required_url_parts)

@checkpoint
def grade_checkpoint2():
    messages = get_rocketchat_channel_history(rocket, "project-ai")
    if not messages:
        return False
    
    keywords = ['bug', 'issues', 'open']

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if all(keyword in message_text for keyword in keywords):
            return True

    return False

def grade_final_checkpoint():
    messages = get_rocketchat_channel_history(rocket, "project-ai")
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
    checkpoints.append(Checkpoint(total=2, result=int(final_result)))

    return result
