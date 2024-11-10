import requests
import logging
import os
import sys
from io import BytesIO

from requests.auth import HTTPBasicAuth
from typing import List
import xml.etree.ElementTree as ET

from odf.opendocument import load
from odf.text import P

from scoring import Result, Checkpoint
from config import NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD


def grade_checkpoint1(trajectory):
    urls = [f"https://ogma.lti.cs.cmu.edu/apps/files/files/575?dir=/Documents/Human%20Resources%20Team"]
            
    return any(url in trajectory for url in urls)


def grade_checkpoint2():
    file_name = "Salary_Increase_MEMO.odt"
    dir_name = "Documents/Human%20Resources%20Team"

    score = 0

    try: 
        if file_exists_in_directory(file_name, dir_name):
            score += 1
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

    try: 
        binary_content = get_binary_file_content(file_name, dir_name)

        if binary_content:
            text_content = extract_text_from_odt(binary_content)

            keywords = ["name", "email", "salary amount", "assignment start and end date"]

            found_keywords, keyword_score = check_keywords_in_content(text_content, keywords)
            print(keyword_score)
            
            if found_keywords:
                print(f"Keywords found in the document: {', '.join(found_keywords)}")
                score += keyword_score

            return score
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0
    

def grade_checkpoint3():
    dir_name = "Documents/Human%20Resources%20Team/salary_increase_notice"
    score = 0
    try: 
        if not directory_exists(dir_name):
            print(f"Directory '{dir_name}' not found.")
            return 0
        else:
            print(f"Directory '{dir_name}' found.")
            score += 1
    except Exception as e:
        print(f"Error: {e}") 
        return 0
    
    file_count = count_files_in_directory(dir_name)
    if file_count == 10:
        print(f"Directory '{dir_name}' contains 10 files.")
        score += 1

    return score
    

def count_files_in_directory(dir_name):
    server_url = f"https://ogma.lti.cs.cmu.edu/remote.php/dav/files/admin/{dir_name}"
    headers = {
        'OCS-APIRequest': 'true',
        'Content-Type': 'application/xml',
        'Depth': '1',
    }

    response = requests.request(
        method="PROPFIND",
        url=server_url,
        headers=headers,
        auth=HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)
    )

    if response.status_code == 207:
        root = ET.fromstring(response.text)
        # Subtract 1 to exclude the directory itself
        return len(root.findall(".//{DAV:}response")) - 1
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return 0
    
def directory_exists(dir_name):
    server_url = f"https://ogma.lti.cs.cmu.edu/remote.php/dav/files/admin/{dir_name}"
    headers = {
        'OCS-APIRequest': 'true',
        'Depth': '0',
    }

    response = requests.request(
        method="PROPFIND",
        url=server_url,
        headers=headers,
        auth=HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)
    )

    return response.status_code == 207


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


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    return result


