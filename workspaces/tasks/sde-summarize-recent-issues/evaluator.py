import requests
import logging
import os
import sys
import json
from typing import List

from common import create_rocketchat_client
from scoring import Result, Checkpoint, bonus_for_completing_final


# Create RocketChat instance
rocket = create_rocketchat_client()

def grade_checkpoint1(trajectory):
    return f"http://the-agent-company.com:8929/root/janusgraph/-/issues/?sort=created_date&state=opened" in trajectory

def grade_checkpoint2():
    messages = get_message("project-graphdb")
    if not messages:
        return False
    
    summary_keywords = ['summary', 'issues', 'August']

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if all(keyword in message_text for keyword in summary_keywords):
            return True

    return False

def grade_final_checkpoint():
    messages = get_message("project-graphdb")
    if not messages:
        return False
    
    summary_content_keywords = ['''g.E('edge-id').valueMap()''', 
                                'java.lang.ExceptionInInitializerError', 
                                'TypeDefinitionCategory',
                                'ModifierType',
                                'ScyllaDB',
                                '6.1.0',
                                'end-of-life',
                                'multi-thread',
                                'concurrent',
                                'Cassandra',
                                ]

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if all(keyword in message_text for keyword in summary_content_keywords):
            return 2
        elif any(keyword in message_text for keyword in summary_content_keywords):
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

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))

    checkpoints.append(Checkpoint(2, 2 * int(grade_final_checkpoint())))    

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))
