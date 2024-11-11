import logging
import os
import sys
from io import BytesIO
from odf.opendocument import load
from odf.element import Node

import json
from typing import List

from common import llm_complete, check_file_in_nextcloud_directory, get_binary_file_content_nextcloud, checkpoint
from scoring import Result, Checkpoint, bonus_for_completing_any
from config import NEXTCLOUD_URL


@checkpoint
def grade_checkpoint1(trajectory):
    urls = [f"{NEXTCLOUD_URL}/apps/files/files/575?dir=/Documents/Human%20Resources%20Team"]
            
    return any(url in trajectory for url in urls)


@checkpoint
def grade_checkpoint2():
    file_name = "Employee_Manual.odt"
    dir_name = "Documents/Human%20Resources%20Team"

    score = 0

    if check_file_in_nextcloud_directory(file_name, dir_name):
        score += 1
    else:
        return 0

    binary_content = get_binary_file_content_nextcloud(file_name, dir_name)

    if binary_content:
        text_content = extract_text_from_odt(binary_content)

        keywords = ["company values", "code of conduct", "operational procedures", "employee benefits", "company policies"]

        found_keywords, keyword_score = check_keywords_in_content(text_content, keywords)
        
        if found_keywords:
            print(f"Keywords found in the document: {', '.join(found_keywords)}")
            score += keyword_score        

        return score
    else:
        print("Failed to retrieve file content.")
        return 0
    
@checkpoint
def grade_checkpoint3():
    file_name = "Employee_Manual.odt"
    dir_name = "Documents/Human%20Resources%20Team"

    score = 0

    binary_content = get_binary_file_content_nextcloud(file_name, dir_name)

    if binary_content:
        text_content = extract_text_from_odt(binary_content)

        messages = [{"content": f"An Employee Manual is provided below: \"\"{text_content}\"\" \n Is the manual formatted for readability, with headings, subheadings, bullet points and table of contents where necessary? Please answer 'yes' if it does, or 'no' if it doesn't. ", "role": "user"}]

        # Check result
        llm_resonse = llm_complete(messages)

        if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
            score += 1            

        return score
    else:
        print("Failed to retrieve file content.")
        return 0
    

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

def check_keywords_in_content(content, keywords):
    content = content.lower()
    found_keywords = [keyword for keyword in keywords if keyword in content]
    score = len(found_keywords) / len(keywords)
    return found_keywords, score

    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))

    return result

