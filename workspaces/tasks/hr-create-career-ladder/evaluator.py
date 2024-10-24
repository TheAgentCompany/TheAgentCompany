import requests
import logging
import os
import sys
from io import BytesIO
from odf.opendocument import load
from odf.element import Node

from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from common import llm_evaluate
from common import create_rocketchat_client

NEXTCLOUD_USERNAME = 'admin'
NEXTCLOUD_PASSWORD = os.environ.get('NEXTCLOUD_ADMIN_PASSWORD')

rocket = create_rocketchat_client()

def grade_checkpoint1(trajectory):
    urls = [f"https://ogma.lti.cs.cmu.edu/apps/files/files/575?dir=/Documents/Human%20Resources%20Team"]
            
    return any(url in trajectory for url in urls)

def grade_checkpoint2():
    file_name = "Career_Ladder.odt"
    dir_name = "Documents/Human%20Resources%20Team"

    score = 0

    binary_content = get_binary_file_content(file_name, dir_name)

    if binary_content:
        text_content = extract_text_from_odt(binary_content)

        messages = [{"content": f"You are asked to grade the following content: \"\"{text_content}\"\" \n Is this a valid career ladder Please answer 'yes' if it does, or 'no' if it doesn't. ", "role": "user"}]

        try: 
            llm_resonse = llm_evaluate(messages)
        except Exception as e:
            print(f"Error: {e}")
            return 0

        if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
            print("Valid career ladder found.")
            score += 1            

        return score
    else:
        print("Failed to retrieve file content.")
        return 0
    
def grade_final_checkpoint():
    messages = get_message("hr-announcements")
    if not messages:
        return False
    
    score = 0

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        messages = [{"content": f"You are asked to grade the following message: \"\"{message_text}\"\" \n Is the message about the new career ladder design and asking for suggestions? Please answer 'yes' if it does, or 'no' if it doesn't. ", "role": "user"}]

        try:
            llm_resonse = llm_evaluate(messages)
        except Exception as e:
            print(f"Error: {e}")
            return 0
        if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
            print("Correct message found.")
            score += 1
            break
    
    return score
    
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

def file_exists_in_directory(file_name, dir_name):
    server_url = f"https://ogma.lti.cs.cmu.edu/remote.php/dav/files/admin/{dir_name}"
    headers = {
        'OCS-APIRequest': 'true',
        'Content-Type': 'application/xml',
        'Depth': '1',  # Depth of 1 to list the immediate contents of the directory
    }

    # Send PROPFIND request
    response = requests.request(
        method="PROPFIND",
        url=server_url,
        headers=headers,
        auth=HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)
    )

    if response.status_code == 207:
        root = ET.fromstring(response.text)
        for response in root.findall(".//{DAV:}response"):
            href = response.find("{DAV:}href").text
            if file_name in href:
                print(f"File '{file_name}' found.")
                return True

        # If loop completes and file is not found
        print(f"File '{file_name}' not found.")
        return False
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def get_binary_file_content(file_name, dir_name):
    server_url = f"https://ogma.lti.cs.cmu.edu/remote.php/dav/files/admin/{dir_name}"
    file_url = f"{server_url}/{file_name}"

    response = requests.get(file_url, auth=HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD))

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def extract_text_from_odt(binary_content):
    odt_file = BytesIO(binary_content)
    document = load(odt_file)

    text_content = ""

    def get_text_from_node(node):
        text = ""
        for child in node.childNodes:
            if isinstance(child, Node):
                if hasattr(child, 'data'):
                    text += child.data + "\n"
                text += get_text_from_node(child)  
        return text

    for elem in document.text.childNodes:
        text_content += get_text_from_node(elem) + "\n"

    return text_content

    
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
    if passed2 or passed3:
        passed1 = 1
    points = sum([passed1, passed2, passed3])
    print("Scores: ", passed1, passed2, passed3)
    print(f"Final points for task Create Employee Manual: {points}")
