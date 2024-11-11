import os

from typing import List

import pandas as pd
from datetime import datetime

from scoring import Result, Checkpoint, bonus_for_completing_final
import logging

from common import create_rocketchat_client, get_rocketchat_personal_chat_history, grader

############################# Init Variables #####################################
# Create RocketChat instance
rocket = create_rocketchat_client()

REFERENCE_MONTH = 'february'

REFERENCE_COST = '65,059.68'


############################# Helper Functions #####################################
def check_file_exists(file_path):
    abs_path = os.path.abspath(file_path)
    try:
        return os.path.isfile(abs_path)
    except Exception as e:
        logging.warning(f"Error in is_file_exist: {e}")
        return False

def read_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except Exception:
        return None

def check_no_over_allocation(plan_df):
    monthly_person_effort = plan_df.groupby(['month', 'person'])['effort percent'].sum()
    return all(monthly_person_effort <= 100)


def check_exact_allocation(plan_df, goal_requirements):
    allocated_effort = plan_df.groupby('role')['effort percent'].sum().to_dict()
    return allocated_effort == goal_requirements

def sort_values_by_month(plan_df):
    plan_df['month'] = pd.Categorical(plan_df['month'], categories=[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"], ordered=True)

    plan_df = plan_df.sort_values(by="month")
    return plan_df

############################# Evaluator #####################################

@grader
def grade_checkpoint1():
    chat_history = get_rocketchat_personal_chat_history(rocket, "Chen Xinyi")
    return len(chat_history) > 0

@grader
def grade_checkpoint2():
    required_urls = [
        # Add required document URLs here
        '/workspace/core_competencies.xlsx',
        '/workspace/Effort Planning 2025.docx',
        '/workspace/salary_benefits_2024.xlsx'
    ]
    return all(check_file_exists(url) for url in required_urls)

@grader
def grade_checkpoint3():
    if not check_file_exists("/workspace/project-plan.csv"):
        return False
    try:
        df = read_csv("/workspace/project-plan.csv")
        df.columns = df.columns.str.lower()
        required_columns = ["month", "person", "effort percent", "role"]
        # Check if all required columns exist
        if not all(col in df.columns for col in required_columns):
            return False
        # Check if all roles are valid
        valid_roles = {'li', 'pm', 'design', 'frontend', 'backend', 'infra'}
        df['role'] = df['role'].str.lower()  # Convert roles to lowercase
        if not df['role'].isin(valid_roles).all():
            return False
            
        return True
    except Exception:
        return False

@grader
def grade_checkpoint4():
    try:
        df = read_csv("/workspace/project-plan.csv")
        df.columns = df.columns.str.lower()
        return check_no_over_allocation(df)
    except Exception:
        return False

@grader
def grade_checkpoint5():
    try:
        df = read_csv("/workspace/project-plan.csv")
        df.columns = df.columns.str.lower()
        goal_requirements = {
            'li': 50,        
            'pm': 50,        
            'design': 50,    
            'frontend': 100, 
            'backend': 150,  
            'infra': 50
        }
        return check_exact_allocation(df, goal_requirements)
    except Exception:
        return False

@grader
def grade_checkpoint6():
    # Check if project ends in earliest possible month
    try:
        df = read_csv("/workspace/project-plan.csv")
        df.columns = df.columns.str.lower()
        sorted_df = sort_values_by_month(df)
        return sorted_df.iloc[-1].month.lower() == 'february'
    except Exception:
        return False

@grader
def grade_checkpoint7():
    chat_history = get_rocketchat_personal_chat_history(rocket, "Sarah Johnson")
    # Add logic to verify correct month was communicated
    for msg in chat_history:
        if str(REFERENCE_MONTH) in msg.lower():
            return True
    return False

@grader
def grade_checkpoint8():
    # Check if Sarah was messaged with correct dollar amount
    chat_history = get_rocketchat_personal_chat_history(rocket, "Sarah Johnson")
    # Add logic to verify correct dollar amount was communicated
    for msg in chat_history:
        if str(REFERENCE_COST) in msg:
            return True
    return False

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    
    checkpoints.append(Checkpoint(1, grade_checkpoint1()))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    checkpoints.append(Checkpoint(1, grade_checkpoint4()))
    checkpoints.append(Checkpoint(1, grade_checkpoint5()))
    checkpoints.append(Checkpoint(1, grade_checkpoint6()))
    checkpoints.append(Checkpoint(1, grade_checkpoint7()))
    checkpoints.append(Checkpoint(1, grade_checkpoint8()))
    
    return result


