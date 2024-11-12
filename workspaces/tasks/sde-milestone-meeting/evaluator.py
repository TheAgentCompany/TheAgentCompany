import requests
import logging
from bs4 import BeautifulSoup
from typing import List


from common import create_rocketchat_client, grader
from scoring import Result, Checkpoint, bonus_for_completing_any


# Create RocketChat instance
rocket = create_rocketchat_client()

@grader
def grade_checkpoint1(trajectory):
    urls = [f"http://the-agent-company.com:8929/root/janusgraph/-/milestones/27#tab-merge-requests",
            f"http://the-agent-company.com:8929/root/janusgraph/-/merge_requests?milestone_title=Release+v1.1.0"]
    return any(url in trajectory for url in urls)

@grader
def grade_checkpoint2():
    url = f"http://the-agent-company.com:8929/root/janusgraph/-/merge_requests/4657"

    try:
        response = requests.get(url)
    except requests.RequestException as e:
        logging.error(f"Error fetching PR: {e}")
        return False

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all("div", class_="js-mr-header")
        for element in elements:
            if element and element['data-state'] == "merged":
                return True
    else:
        logging.error(f"Failed to fetch the webpage: {response.status_code}")

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
        if all(keyword in message_text for keyword in merge_conflit):
            score[1] = 1
        if "4456" in message_text:
            score[2] = 1
    
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
    
    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    passed_checkpoint1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, passed_checkpoint1))

    passed_checkpoint2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, passed_checkpoint2))

    passed_final_checkpoint = grade_final_checkpoint()
    checkpoints.append(Checkpoint(1, passed_final_checkpoint))

    return result


