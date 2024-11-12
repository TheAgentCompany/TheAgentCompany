import requests
import logging
import os
import sys

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, grader

# Create RocketChat instance
rocket = create_rocketchat_client()

@grader
def grade_checkpoint1(trajectory):
    return f"http://the-agent-company.com:8929/root/janusgraph/-/issues/?sort=priority_desc&state=opened&first_page_size=20" in trajectory

@grader
def grade_checkpoint2():
    messages = get_message("janusgraph")
    if not messages:
        return False
    
    followup_keywords = ['follow up', 'issues', 'gitlab repo']

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if all(keyword in message_text for keyword in followup_keywords):
            return True

    return False

def grade_final_checkpoint():
    messages = get_message("janusgraph")
    if not messages:
        return False
    
    followup_keywords = ['4641', '4658', '4622', '4595', '4583']

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if all(keyword in message_text for keyword in followup_keywords):
            return 2
        elif any(keyword in message_text for keyword in followup_keywords):
            return 1
    
    return False
    
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
    
    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_final_checkpoint()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    return result



