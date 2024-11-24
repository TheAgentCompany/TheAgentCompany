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
from config import OWNCLOUD_URL, OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD
from common import grader, check_file_in_owncloud_directory, get_binary_file_content_owncloud



@grader
def grade_checkpoint1(trajectory):
    urls = [f"dir=/Documents/Human%20Resources%20Team"]
            
    return any(url in trajectory for url in urls)


@grader
def grade_checkpoint2():
    file_name = "Salary_Increase_MEMO.odt"
    dir_name = "Documents/Human%20Resources%20Team"

    score = 0

    try: 
        if check_file_in_owncloud_directory(file_name, dir_name):
            score += 1
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

    try: 
        binary_content = get_binary_file_content_owncloud(file_name, dir_name)

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
    

@grader
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
    server_url = f"{OWNCLOUD_URL}/remote.php/webdav/{dir_name}"
    headers = {
        'Depth': '1',
    }

    try:
        response = requests.request(
            method="PROPFIND",
            url=server_url,
            headers=headers,
            auth=HTTPBasicAuth(OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD)
        )
    except requests.RequestException as e:
        logging.warning(f"Failed to count files in owncloud directory: {e}")
        return 0

    if response.status_code == 207:
        root = ET.fromstring(response.text)
        # Subtract 1 to exclude the directory itself
        return len(root.findall(".//{DAV:}response")) - 1
    else:
        logging.error(f"Error: {response.status_code}, {response.text}")
        return 0

def directory_exists(dir_name):
    server_url = f"{OWNCLOUD_URL}/remote.php/webdav/{dir_name}"
    headers = {
        'Depth': '0',
    }

    try:
        response = requests.request(
            method="PROPFIND",
            url=server_url,
            headers=headers,
            auth=HTTPBasicAuth(OWNCLOUD_USERNAME, OWNCLOUD_PASSWORD)
        )
    except requests.RequestException as e:
        logging.warning(f"Failed to check directory existence in owncloud: {e}")
        return False

    return response.status_code == 207


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
    checkpoints.append(Checkpoint(2, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint3())))
    return result


