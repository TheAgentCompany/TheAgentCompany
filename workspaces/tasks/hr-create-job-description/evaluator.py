import requests
import logging
import os
import sys
from io import BytesIO
from odf.opendocument import load
from odf.text import P

from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from rocketchat_API.rocketchat import RocketChat # type: ignore

HOSTNAME = os.getenv('HOSTNAME') or 'ogma.lti.cs.cmu.edu'
NEXTCLOUD_USERNAME = 'admin'
NEXTCLOUD_PASSWORD = os.environ.get('NEXTCLOUD_ADMIN_PASSWORD')

ROCKETCHAT_PORT = os.getenv('ROCKETCHAT_PORT') or '3000'
ROCKETCHAT_URL = f"http://{HOSTNAME}:{ROCKETCHAT_PORT}"
ADMIN_USERNAME = 'jobbench'
ADMIN_PASS = 'jobbench'

rocket = RocketChat(ADMIN_USERNAME, ADMIN_PASS, server_url=ROCKETCHAT_URL)


def grade_checkpoint1(trajectory):
    urls = [f"https://ogma.lti.cs.cmu.edu/apps/files/files/575?dir=/Documents/Human%20Resources%20Team&openfile=true"]
            
    return any(url in trajectory for url in urls)

def grade_checkpoint2():
    messages = get_message("project-ai")
    if not messages:
        return False
    
    keywords = ["tech skills", "tech stack", "required skills", "preferred skills"]
    score = 0

    for msg in messages:
        message_text = msg.get('msg', '').lower()
        if any(keyword in message_text for keyword in keywords):
            score += 1
    
    return score


def grade_checkpoint3():
    file_name = "Entry_SDE_JD.odt"
    dir_name = "Documents/Human%20Resources%20Team/"

    score = 0

    if file_exists_in_directory(file_name, dir_name):
        score += 1
    else:
        return 0

    binary_content = get_binary_file_content(file_name, dir_name)

    if binary_content:
        text_content = extract_text_from_odt(binary_content)

        required_sections = ["title", "location", "responsibilities", "requirements", "preferred skills", "benefits"]
        found_keywords, keyword_score = check_keywords_in_content(text_content, required_sections)
        
        if found_keywords:
            print(f"Keywords found in the document: {', '.join(found_keywords)}")
            score += keyword_score

        tech_skills = ["react", "node.js", "sql", "restful apis"]

        found_keywords, tech_keyword_score = check_keywords_in_content(text_content, tech_skills)
        
        if found_keywords:
            print(f"Tech SkillsKeywords found in the document: {', '.join(found_keywords)}")
            score += tech_keyword_score

        return score
    else:
        print("Failed to retrieve file content.")
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


def get_binary_file_content(dir_name, file_name):
    server_url = f"https://ogma.lti.cs.cmu.edu/remote.php/dav/files/admin/{dir_name}/{file_name}"
    file_url = f"{server_url}{file_name}"

    response = requests.get(file_url, auth=HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD))

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def extract_text_from_odt(binary_content):
    # Load the binary content into a BytesIO stream
    odt_file = BytesIO(binary_content)
    document = load(odt_file)

    text_content = ""
    for paragraph in document.getElementsByType(P):
        if paragraph.firstChild is not None:
            text_content += str(paragraph.firstChild) + "\n"

    return text_content

def check_keywords_in_content(content, keywords):
    content = content.lower()
    found_keywords = [keyword for keyword in keywords if keyword in content]
    score = len(found_keywords) / len(keywords)
    return found_keywords, score

    
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
    passed3 = grade_checkpoint3()
    points = sum([passed1, passed2, passed3])
    print(f"Final points for task Create Job Description: {points}")
