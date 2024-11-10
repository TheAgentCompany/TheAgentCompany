import logging
import numpy as np
import pandas as pd

from common import evaluate_chat_history_with_llm, create_rocketchat_client, grader
from scoring import Result, Checkpoint


LOCAL_XLSX = "/workspace/merged.xlsx"
NPC_NAME = "wang_fang"
sheet1 = [
    [1, ["Fruit", "not", "containing", "free", "sugars"], 16.6, 15.2, 18, 17.7, 16.2, 19.2],
    [2,	["Milk", "not", "containing", "free", "sugars"], 16.4, 15.2, 17.5, 13.6, 12.5, 14.8],
    [3, ["Juice", "containing", "free", "sugars"], 16.8, 15.3, 18.3, 11.6, 10.3, 12.9],
    [4, ["Regular", "soft", "drinks", "containing", "free", "sugars"], 15.9, 14.6, 17.1, 7, 5.8, 8.2],
    [5, ["Sugars", "syrups", "and", "confectionary", "containing", "free", "sugars"], 13, 11.6, 14.5, 9.4, 8.2, 10.5],
    [6, ["Baked", "goods", "and", "products", "containing", "free", "sugars"], 6, 5.2, 6.9, 8.9, 7.6, 10.1],
    [7, ["Frozen", "desserts", "containing", "free", "sugars"], 4.1, 3.2, 5, 6.3, 4.5, 8.2],
    [8, ["Yoghurt", "containing", "free", "sugars"], 2, 1.4, 2.6, 5.7, 4.9, 6.6],
    [9, ["Vegetables", "not", "containing", "free", "sugars"], 2.7, 2.5, 3, 2.6, 2.3, 2.9],
    [10, ["Fruit", "drinks", "containing", "free", "sugars"], 6.3, 5.2, 7.4, 3.5, 2.5, 4.5],
    [11, ["Vegetables", "not", "containing", "free", "sugars"], 2.7, 2.5, 3, 2.6, 2.3, 2.9]
]

def found_matching_row(df, sheet: list):
    if df is None:
        return False
    try:
        for entry in sheet:
            column = 0
            cond = True
            for keywords in entry:
                if isinstance(keywords, list):
                    for key in keywords:
                        cond &= df.iloc[:, column].str.contains(key, case=False)
                elif np.isnan(keywords):
                    cond &= df.iloc[:, column].isna()
                else:
                    cond &= df.iloc[:, column] == keywords

                column += 1
            matching_rows = df[cond]
            if matching_rows.empty:
                return False
    except Exception as e:
        logging.error("Error finding matching row: %s", e)
    return True

def read_sheet(sheet_index: int):
    try:
        df = pd.read_excel(LOCAL_XLSX, sheet_name=sheet_index)
    except Exception as e:
        logging.error("Error reading sheet %s: %s", sheet_index, e)
        return None
    return df

@grader
def grade_checkpoint1():
    """Propose merging the sheets on Rocketchat"""
    rocket_client = create_rocketchat_client()
    return evaluate_chat_history_with_llm(rocket_client, NPC_NAME, "a proposal of merging the data")

@grader
def grade_checkpoint2():
    return found_matching_row(read_sheet(0), sheet1)

def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(1, 1*int(grade_checkpoint1()))
    checkpoint2 = Checkpoint(2, 2*int(grade_checkpoint2()))
    return Result([checkpoint1, checkpoint2])
