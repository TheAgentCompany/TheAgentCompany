import os

from typing import List

import pandas as pd
from datetime import datetime

from scoring import Result, Checkpoint, bonus_for_completing_final
import logging


def check_excel_file_exists(file_path):
    abs_path = os.path.abspath(file_path)
    try:
        return os.path.isfile(abs_path)
    except Exception as e:
        logging.warning(f"Error in is_file_exist: {e}")
        return False


def read_excel(filename):
    try:
        df = pd.read_excel(filename)
        names = set(df['Name'].tolist())
        return names
    except Exception:
        return None


def filter_name(filename):
    try:
        df = pd.read_csv(filename)

        # Strip out the spaces if there are any
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        df['Clock-out'] = pd.to_datetime(df['Clock-out'], format='%H:%M').dt.time

        start_time = datetime.strptime("17:30", "%H:%M").time()
        end_time = datetime.strptime("18:00", "%H:%M").time()

        filtered_df = df[(df['Clock-out'] >= start_time) & (df['Clock-out'] <= end_time)]
        return set(filtered_df['Name'].tolist())
    except Exception:
        return None


def grade_checkpoint1(trajectory):
    urls = [f"/apps/files/files/1225?dir=/Documents/Human%20Resources%20Team/Attendance"]
    return any(url in trajectory for url in urls)


def grade_checkpoint2():
    if not check_excel_file_exists("/workspace/2024-03-attendance-summary.xlsx"):
        return False
    try:
        df = pd.read_excel("/workspace/2024-03-attendance-summary.xlsx")
        return "Name" in df.columns
    except Exception:
        return False


def grade_checkpoint3():
    name = read_excel("/workspace/2024-03-attendance-summary.xlsx")
    correct_answer = filter_name('/utils/attendance-2024-03-01.csv')
    if name is None or correct_answer is None:
        return False
    if name == correct_answer:
        return True
    return False


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    return result
