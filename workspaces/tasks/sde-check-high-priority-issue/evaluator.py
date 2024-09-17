import requests
import logging
import os
import sys
from rocketchat_API.rocketchat import RocketChat # type: ignore

HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
channel_name = "general"
ROCKETCHAT_URL = f"http://{HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

def grade_checkpoint1(trajectory):
    return f"http://ogma.lti.cs.cmu.edu:8929/root/janusgraph/-/issues/?sort=priority_desc&state=opened&first_page_size=20" in trajectory

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
            return True
        elif any(keyword in message_text for keyword in followup_keywords):
            return 0.5
    
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
    points = 4 if passed3 else int(passed1) + int(passed2)
    print(f"Final points for task Example: {points}")
