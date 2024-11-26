import logging
from typing import List
from io import BytesIO
import pandas as pd
from collections import defaultdict

from common import create_rocketchat_client, check_file_in_owncloud_directory, get_binary_file_content_owncloud, evaluate_chat_history_with_llm, grader
from scoring import Result, Checkpoint

rocket = create_rocketchat_client()
employees_involved = [
    "Sarah Johnson","Li Ming","Zhang Wei","Wang Fang",
    "Mike Chen","Emily Zhou","Liu Qiang","Priya Sharma",
    "Mark Johnson","Jessica Lee","Chen Xinyi","David Wong",
    "Huang Jie","Sophia Rodriguez","Alex Turner","Emma Lewis","Jessica Chen"
]

@grader
def grade_checkpoint1():
    file_name = "YearEnd_Vacation_Survey.xlsx"
    dir_name = "Documents/Human%20Resources%20Team"
    if not check_file_in_owncloud_directory(file_name, dir_name):
        return 0

    content = get_binary_file_content_owncloud(file_name, dir_name)
    if not content:
        logging.warning("Failed to download content")
        return 0

    try:
        survey_results = pd.read_excel(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read {file_name}: {e}")
        return 0
    
    required_columns = ["Name", "Gender", "Age", "Role", "Vacation_Destination", "Number_of_Vacation_Days", "Expected_Travel_Budget"]
    if not all(column in survey_results.columns for column in required_columns):
        return 0
    
    solution = pd.read_excel("/utils/solution.xlsx")
    expected_data = solution.iloc[:-1].set_index("Name").T.to_dict()
    expected_data = {key.lower(): value for key, value in expected_data.items()}

    correct_rows = defaultdict(int)
    res = len(expected_data) + 1

    for _, row in survey_results.iterrows():
        name = row["Name"].lower()
        if name in expected_data:
            expected_row = expected_data[name]
            row_correct = all(row[col] == expected_row[col] for col in expected_row)
            
            correct_rows[name] = row_correct
    
    score = sum(correct_rows.values())

    # check for total budget correctness
    if solution["Expected_Travel_Budget"].iloc[-1] == survey_results["Expected_Travel_Budget"].iloc[-1]:
        score += 1
    
    if score == res:
        return 5
    else:
        return round((score / res) * 5)


@grader
def grade_checkpoint2():
    res = 0
    for employee in employees_involved:
        ans = evaluate_chat_history_with_llm(rocket, employee, "This person has been asked about their year-end vacation plans")
        res += int(ans)

    if res == len(employees_involved):
        return 2
    else:
        return 1

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = [
        Checkpoint(5, int(grade_checkpoint1())),
        Checkpoint(2, int(grade_checkpoint2())),
    ]
    result = Result(checkpoints)
    return result
