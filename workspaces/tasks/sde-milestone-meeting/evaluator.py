import requests
import logging
import os
import sys
from rocketchat_API.rocketchat import RocketChat # type: ignore
from bs4 import BeautifulSoup

HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
channel_name = "general"
ROCKETCHAT_URL = f"http://{HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

def grade_checkpoint1(trajectory):
    urls = [f"http://ogma.lti.cs.cmu.edu:8929/root/janusgraph/-/milestones/27#tab-merge-requests",
            f"http://ogma.lti.cs.cmu.edu:8929/root/janusgraph/-/merge_requests?milestone_title=Release+v1.1.0"]
    return any(url in trajectory for url in urls)

def grade_checkpoint2():
    url = f"http://ogma.lti.cs.cmu.edu:8929/root/janusgraph/-/merge_requests/4657"
    pat = os.getenv("GITLAB_ACCESS_TOKEN")

    headers = {
        'PRIVATE-TOKEN': pat
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all("div", class_="js-mr-header")
        for element in elements:
            if element and element['data-state'] == "merged":
                return True
    else:
        print(f"Failed to fetch the webpage: {response.status_code}")

    return False

def grade_final_checkpoint():
    messages = get_message("janusgraph")
    if not messages:
        return False
    
    meeting_agenda = ['release v1.1.0', 'milestone']
    merge_conflit = ['conflict', 'merge', 'request']
    score = [0] * 3

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if all(keyword in message_text for keyword in meeting_agenda):
            score[0] = 1
            continue
        if all(keyword in message_text for keyword in merge_conflit):
            score[1] = 1
            continue
        if "4456" in message_text:
            score[2] = 1
            continue 
    
    return sum(score)
    
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
    points = sum([passed1, passed2, passed3])
    print(f"Final points for task Check High Priority Issue: {points}")
