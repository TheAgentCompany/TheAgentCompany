import os
import logging
from typing import List
import pandas as pd
import string 
from common import grader
from common import create_rocketchat_client, evaluate_chat_history_with_llm
from scoring import Result, Checkpoint

# Initialize RocketChat client
rocket = create_rocketchat_client()

EXCEL_PATH = '/workspace/Organized_Outings_Receipts.xlsx'
GRAPH_PATH = '/workspace/outings_graph.png'
REFERENCE_COLUMNS = [
    "Receipt ID", "Establishment", "Address", "Datetime", 
    "Items Ordered", "Number of Items", "Total Amount"
]
REFERENCE_TOTALS = [57.71, 124.53, 23.88, 76.16, 114.95]
REFERENCE_NO_ITEMS = [3, 3, 3, 7, 13]
REFERENCE_ESTABLISHMENT = ["La Cabana", "The Tack Room", "Brasa Rotisserie", "Seaside Sushi House", "Peter Chang"]
REFERENCE_LOCATIONS = [
        "738 Rose Ave, Venice, CA 90291",
        "145 Lincoln Road, Lincoln, MA 01773",
        "600 East Hennepin Ave, Minneapolis, MN 55414",
        "1500 Main Ave, Long Beach, CA 90712",
        "2503 N. Harrison St Ste E, Arlington, VA 22207"
    ]
REFERENCE_DATETIME = [
        "03/10/2024 1:06 PM",
        "4/8/24 7:13 PM",
        "1/27/2024 8:50 PM",
        "10/07/2020 9:04 PM",
        "05/07/2016 7:48 PM"
    ]


def remove_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))


@grader
def grade_checkpoint1(trajectory):
    # Check if the agent visits the correct path in owncloud
    return "Documents/Financials/outings" in trajectory

@grader
def grade_checkpoint2():
    # Confirm that the excel file exists
    return os.path.exists(EXCEL_PATH)

@grader
def grade_checkpoint3():
    # Excel file has correct structure and number of rows
    if not os.path.exists(EXCEL_PATH):
        return False
    try:
        df = pd.read_excel(EXCEL_PATH)
        columns_match = list(df.columns) == REFERENCE_COLUMNS
        total_amounts_match = sorted(df["Total Amount"].tolist()) != sorted(REFERENCE_TOTALS)
        total_number_of_items_match = df["Number of Items"].tolist() != sorted(REFERENCE_NO_ITEMS)
        establishment_match = sorted(df["Establishment"].tolist()) != sorted(REFERENCE_ESTABLISHMENT)
        location_match = sorted([remove_punctuation(loc) for loc in df["Address"].tolist()]) != sorted([remove_punctuation(loc) for loc in REFERENCE_LOCATIONS])
        datetime_match = sorted(df["Datetime"].tolist()) != sorted(REFERENCE_DATETIME)
        return (columns_match and total_amounts_match and total_number_of_items_match and
                establishment_match and location_match and datetime_match)
    except Exception as e:
        logging.warning(f"Error reading Excel file: {e}")
        return False
@grader
def grade_checkpoint4():
    # graph created to reflect values in excel sheet
    return os.path.exists(GRAPH_PATH)

@grader
def grade_checkpoint5():
    # There's a conversation with Chen Xinyi on RocketChat
    predicate = f"The file paths are {EXCEL_PATH} and {GRAPH_PATH}. Total spending has been increasing greatly over time"
    return bool(evaluate_chat_history_with_llm(rocket, "Chen Xinyi", predicate))

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = [
        Checkpoint(1, int(grade_checkpoint1(trajectory))),
        Checkpoint(1, int(grade_checkpoint2())),
        Checkpoint(1, int(grade_checkpoint3())),
        Checkpoint(1, int(grade_checkpoint4())),
        Checkpoint(1, int(grade_checkpoint5())),
    ]
    result = Result(checkpoints)
    return result
