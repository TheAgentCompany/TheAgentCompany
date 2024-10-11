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
    required_url_parts = [
        "http://ogma.lti.cs.cmu.edu:8929/root/OpenHands/-/issues/",
        "label_name[]=bug",
        "sort=created_date",
        "state=opened",
        "first_page_size=20"
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
    
    issue_numbers = ['#4166', '#4164', '#4157', '#4158', '#4153', '#4131', '#4127']
    required_info = ['issue', 'title', 'assigned', 'http']
    
    for msg in messages:
        message_text = msg.get('msg', '').lower()
        issues_present = sum(1 for num in issue_numbers if num.lower() in message_text)
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
    
    points = 0
    if passed3 == 2:
        points = 4
    elif passed3 == 1:
        points = 3
    else:
        points = int(passed1) + int(passed2)
    
    print(f"Final points for task Check High Priority Issue: {points}")
