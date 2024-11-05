import os

from typing import List

import pandas as pd
from datetime import datetime

from scoring import Result, Checkpoint, bonus_for_completing_final
import logging

from common import create_rocketchat_client, get_rocketchat_personal_chat_history

############################# Init Variables #####################################
# Create RocketChat instance
rocket = create_rocketchat_client()

############################# Helper Functions #####################################
def check_csv_file_exists(file_path):
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
############################# Evaluator #####################################

# Check if Xinyi was contacted about docs
def grade_checkpoint1():
    chat_history = get_rocketchat_personal_chat_history(rocket, "Chen Xinyi")
    return len(chat_history) > 0

# Check if docs were downloaded
def grade_checkpoint2(trajectory):
    required_urls = [
        # Add required document URLs here
    ]
    return all(url in trajectory for url in required_urls)

# Check if project-plan.csv exists and has correct format
def grade_checkpoint3():
    if not check_csv_file_exists("/workspace/project-plan.csv"):
        return False
    try:
        df = read_csv("/workspace/project-plan.csv")
        df.columns = df.columns.str.lower()
        required_columns = ["month", "person", "effort"]
        return all(col in df.columns for col in required_columns)
    except Exception:
        return False

# Check no person is allocated more than 100% in any month
def grade_checkpoint4():
    try:
        df = read_csv("/workspace/project-plan.csv")
        monthly_allocation = df.groupby(['Month', 'Person'])['Effort'].sum()
        return all(allocation <= 100 for allocation in monthly_allocation)
    except Exception:
        return False

# Check if effort matches project plan requirements
def grade_checkpoint5():
    try:
        df = read_csv("/workspace/project-plan.csv")
        # Add logic to compare against required effort
        return True
    except Exception:
        return False

def grade_checkpoint6():
    # Check if project ends in earliest possible month
    try:
        df = read_csv("/workspace/project-plan.csv")
        # Add logic to verify earliest possible end month
        return True
    except Exception:
        return False

# Check if Sarah was messaged with correct ending month
def grade_checkpoint7():
    chat_history = get_rocketchat_personal_chat_history(rocket, "Sarah Johnson")
    # Add logic to verify correct month was communicated
    return len(chat_history) > 0

def grade_checkpoint8():
    # Check if Sarah was messaged with correct dollar amount
    chat_history = get_rocketchat_personal_chat_history(rocket, "Sarah Johnson")
    # Add logic to verify correct dollar amount was communicated
    return len(chat_history) > 0

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    
    checkpoints.append(Checkpoint(1, grade_checkpoint1()))
    checkpoints.append(Checkpoint(1, grade_checkpoint2(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    checkpoints.append(Checkpoint(1, grade_checkpoint4()))
    checkpoints.append(Checkpoint(1, grade_checkpoint5()))
    checkpoints.append(Checkpoint(1, grade_checkpoint6()))
    checkpoints.append(Checkpoint(1, grade_checkpoint7()))
    checkpoints.append(Checkpoint(1, grade_checkpoint8()))
    
    return result


