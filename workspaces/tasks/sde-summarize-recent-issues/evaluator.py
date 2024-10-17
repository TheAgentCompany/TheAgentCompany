import requests
import logging
import os
import sys
from rocketchat_API.rocketchat import RocketChat # type: ignore

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
channel_name = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

def grade_checkpoint1(trajectory):
    return f"http://ogma.lti.cs.cmu.edu:8929/root/janusgraph/-/issues/?sort=created_date&state=opened" in trajectory

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
    
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, partial credit might not be granted")
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)

    passed1 = grade_checkpoint1(trajectory)
    passed2 = grade_checkpoint2()
    passed3 = grade_final_checkpoint()
    points = (int(passed3) + 2) if passed3 >= 1 else int(passed1) + int(passed2)
    print(f"Final points for task Check High Priority Issue: {points}")
