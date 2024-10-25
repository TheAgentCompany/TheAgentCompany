import requests
import logging
import os
import sys
from rocketchat_API.rocketchat import RocketChat # type: ignore
from bs4 import BeautifulSoup
import subprocess

SERVER_HOSTNAME = os.getenv('SERVER_HOSTNAME') or 'ogma.lti.cs.cmu.edu'
ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
channel_name = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)

def grade_checkpoint1():
    url = f"http://ogma.lti.cs.cmu.edu:8929/root/sotopia/-/merge_requests/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all("div", class_="js-mr-header")
        for element in elements:
            if element and element['data-state'] == "merged":
                return True
    else:
        print(f"Failed to fetch the webpage: {response.status_code}")

    return False

def grade_checkpoint2():
    url = "http://ogma.lti.cs.cmu.edu:8929/root/sotopia/-/blob/main/sotopia/agents/llm_agent.py?ref_type=heads"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the code content
        code_block = soup.find('table', class_="highlight")
        
        if code_block:
            # Check if the class NonVerbalAgent exists in the code block
            code_text = code_block.get_text()
            if "class NonVerbalAgent" in code_text:
                return True
    else:
        print(f"Failed to fetch the webpage: {response.status_code}")

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
    points = int(passed1) + int(passed2)
    print(f"Final points for task Sotopia Create Agent: {points}")
