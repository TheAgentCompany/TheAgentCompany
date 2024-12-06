from io import BytesIO
from odf.opendocument import load
from odf.text import P

from typing import List

import pandas as pd

from scoring import Result, Checkpoint, bonus_for_completing_any
from common import grader, check_file_in_owncloud_directory, get_binary_file_content_owncloud


def calculate_salary_statistics(file_path):
    df = pd.read_csv(file_path)
    average_salary = df['Salary'].mean()
    highest_salary = df['Salary'].max()
    lowest_salary = df['Salary'].min()
    median_salary = df['Salary'].median()
    
    return [int(average_salary), int(highest_salary), int(lowest_salary), int(median_salary)]

    
@grader
def grade_checkpoint1():
    file_name = "Salary_Analysis_Report.odt"
    dir_name = "Documents/Human%20Resources%20Team"

    try:
        binary_content = get_binary_file_content_owncloud(file_name, dir_name)

        if binary_content:
            text_content = extract_text_from_odt(binary_content)

            keywords = calculate_salary_statistics("/utils/salary.txt")
            print(f"Keywords: {keywords}")
            
            found_keywords, keyword_score = check_keywords_in_content(text_content, keywords)
            
            if found_keywords:
                print(f"Keywords found in the document: {', '.join(found_keywords)}")
            
            return keyword_score
        else:
            return 0
        
    except Exception as e:
        print("Failed to retrieve file content.")
        print(f"Error: {e}")
        return 0


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
    found_keywords = [str(keyword) for keyword in keywords if str(keyword) in content]
    score = len(found_keywords) / len(keywords)
    return found_keywords, score


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)
    checkpoints.append(Checkpoint(2, int(grade_checkpoint1()*2) ))
    return result



