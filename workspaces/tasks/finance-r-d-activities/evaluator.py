import pandas as pd
import logging
from typing import List
from collections import defaultdict
import numpy as np
from io import BytesIO

from common import create_rocketchat_client, evaluate_chat_history_with_llm, check_file_in_nextcloud_directory, get_binary_file_content_nextcloud, grader
from scoring import Result, Checkpoint

employees_involved = ["Sarah Johnson","Li Ming","Zhang Wei","Wang Fang",
    "Mike Chen","Emily Zhou","Liu Qiang","Sophia Rodriguez","Alex Turner","Emma Lewis"]

rocket = create_rocketchat_client()

@grader
def grade_checkpoint1():
    # check if the all employees in employees_involved are contacted in rocketchat
    res = 0
    for employee in employees_involved:
        ans = evaluate_chat_history_with_llm(rocket, employee, "This person has been asked about their weekly hours on R&D related activities")
        res += int(ans)

    if res == 10:
        return 2
    elif res > 0:
        return 1

@grader
def grade_checkpoint2():
    file_name = "Research_Time_Tracking_Records.csv"
    dir_name = "Documents/Financials"
    if not check_file_in_nextcloud_directory(file_name, dir_name):
        return 0

    content = get_binary_file_content_nextcloud(file_name, dir_name)
    if not content:
        logging.warning("Failed to download content")
        return 0

    # read content as df
    try:
        collected_df = pd.read_csv(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read Research_Time_Tracking_Records.csv: {e}")
        return 0

    required_columns = ["Employee", "Hours_spent", "Qualified_R&D_activities", "R&D_wage"]
    if not all(column in collected_df.columns for column in required_columns):
        return 0
    
    score = 0
    solutions_df = pd.read_csv("/utils/utils.csv")
    # create a employee - hour dictionary
    employee_hours = defaultdict(float)
    for index, row in solutions_df.iterrows():
        if not row["Employee"] == "TOTAL":
            employee_hours[row["Employee"]] = row["Hours_spent"]
    employee_wage = defaultdict(float)
    for index, row in solutions_df.iterrows():
        if not row["Employee"] == "TOTAL":
            employee_wage[row["Employee"]] = row["R&D_wage"]

    # Check if the individual hours are correct, grant partial score if more than 50% of the hours are correct
    correct_hours = 0
    for index, row in collected_df.iterrows():
        if float(row["Hours_spent"]) == employee_hours[row["Employee"]]:
            correct_hours += 1
    if correct_hours == 10:
        score += 2
    elif correct_hours >= 5:
        score += 1

    # Check if the last row is the total wages, if not grant partial score if more than 50% of the wages are correct
    total_wages = collected_df["R&D_wage"].iloc[-1]
    if float(total_wages) == solutions_df["R&D_wage"].iloc[-1]:
        score += 2
    else:
        correct_wages = 0
        for index, row in collected_df.iterrows():
            if float(row["R&D_wage"]) == employee_wage[row["Employee"]]:
                correct_wages += 1
        if correct_wages == 10:
            score += 2
        elif correct_wages >= 5:
            score += 1
    
    return score

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(2, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(4, int(grade_checkpoint2())))

    return result

