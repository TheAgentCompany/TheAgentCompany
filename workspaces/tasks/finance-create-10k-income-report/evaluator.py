import os
import pandas as pd
import numpy as np
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, evaluate_chat_history_with_llm, grader


# Create RocketChat instance
rocket = create_rocketchat_client()

# Reference solution
REFERENCE_CSV = "/utils/reference_net_income.csv"
REFERENCE_NEXTCLOUD_PATH = "/Documents/Data%20Analysis/Annual%20Reports/10Ks"
REFERENCE_FILE_PATH = '/workspace/net_income_report.csv'
REFERENCE_COMPANY = 'Meta Platforms, Inc.'


def check_file_exists(file_path):
    abs_path = os.path.abspath(file_path)
    return os.path.isfile(abs_path)


@grader
def grade_checkpoint1(trajectory):
    # Confirm if the agent navigated to the correct directory
    return REFERENCE_NEXTCLOUD_PATH in trajectory

@grader
def grade_checkpoint2():
    # Check for the existence of 'net_income_report.csv'
    return check_file_exists(REFERENCE_FILE_PATH)

@grader
def grade_checkpoint3():
    # Check if the reported table has the correct structure and format
    file_path = REFERENCE_FILE_PATH
    if not check_file_exists(file_path):
        return False

    # Try reading the CSV with both quote characters
    try:
        df = pd.read_csv(file_path, delimiter=',', quotechar='"')
    except pd.errors.ParserError:
        try:
            df = pd.read_csv(file_path, delimiter=',', quotechar="'")
        except pd.errors.ParserError:
            return False
        
    required_columns = [
        'Company Name', 
        'Net Income - 2021 ($M)', 
        'Net Income - 2022 ($M)', 
        'Net Income - 2023 ($M)', 
        'Percentage Change 2021 - 2022', 
        'Percentage Change 2022 - 2023'
    ]
    reference_df = df = pd.read_csv(file_path, delimiter=',', quotechar='"')
    expected_company_names = reference_df['Company Name'].tolist()
    
    matches_required_columns = all(col in df.columns for col in required_columns)
    matches_company_names = all(company in df['Company Name'].values for company in expected_company_names)

    return matches_company_names and matches_required_columns


@grader
def grade_checkpoint4():
    # Checks if numbers and calculations are performed correctly
    file_path = REFERENCE_FILE_PATH
    if not check_file_exists(file_path):
        return False

    df = pd.read_csv(file_path)
    ref_df = pd.read_csv(REFERENCE_CSV)

    if set(df.columns) != set(ref_df.columns):
        return False
    
    df_set = set(tuple(row) for row in df.to_numpy())
    ref_df_set = set(tuple(row) for row in ref_df.to_numpy())

    return df_set == ref_df_set

@grader
def grade_checkpoint5():
    # Verify if David Wong was contacted with the correct file path and company with highest growth
    predicate = f'The path file mentioned was {REFERENCE_FILE_PATH} and the company with highest growth was {REFERENCE_COMPANY}' 
    chat_history_result = evaluate_chat_history_with_llm(rocket, "David Wong", predicate)
    return chat_history_result

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint5())))
    
    return result
