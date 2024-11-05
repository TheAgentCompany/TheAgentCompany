import logging
import numpy as np
import pandas as pd

from common import get_nextcloud_url_in_file, download_nextcloud_content
from scoring import Result, Checkpoint, bonus_for_completing_final


LINK_FILE = "/workspace/link.txt"
LOCAL_DST = "/workspace/openhands_evaluation.xlsx"

sheet1 = [
    [["Lemur"], ["Lemur-chat-70b"], np.nan, 5.3, np.nan, np.nan],
    [["CodeActAgent", "v1.8"], ["claude-3-5-sonnet"], 26.0, 15.3, 52.0, np.nan]
]

sheet2 = [
    [["SWE-agent", "1-shot"], ["gpt-4-turbo"], 87.7, np.nan],
    [["OH", "CodeActAgent", "v1.5"], ["gpt-3.5-turbo-16k-0613"], 20.1, 0.11]
]

sheet3 = [
    [["WebArena", "Agent"], ["Llama3-chat-70b"], 7.0, np.nan],
]

sheet4 = [
    [["OH", "CodeActAgent", "v1.5"], ["gpt-3.5-turbo-0125"], 11.8, 0.006]
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
        df = pd.read_excel(LOCAL_DST, sheet_name=sheet_index)
    except Exception as e:
        logging.error("Error reading sheet %s: %s", sheet_index, e)
        return None
    return df

def grade_checkpoint1(link):
    if not link:
        return False
    return True

def grade_checkpoint2():
    return found_matching_row(read_sheet(0), sheet1)

def grade_checkpoint3():
    return found_matching_row(read_sheet(1), sheet2)

def grade_checkpoint4():
    return found_matching_row(read_sheet(2), sheet3)

def grade_checkpoint5():
    return found_matching_row(read_sheet(3), sheet4)

def grade_checkpoints(trajectory="") -> Result:
    xlsx_link = get_nextcloud_url_in_file(LINK_FILE)
    download_nextcloud_content(xlsx_link, LOCAL_DST)
    checkpoint1 = Checkpoint(1, 1*int(grade_checkpoint1(xlsx_link)))
    checkpoint2 = Checkpoint(1, 1*int(grade_checkpoint2()))
    checkpoint3 = Checkpoint(1, 1*int(grade_checkpoint3()))
    checkpoint4 = Checkpoint(1, 1*int(grade_checkpoint4()))
    checkpoint5 = Checkpoint(1, 1*int(grade_checkpoint5()))
    return Result([checkpoint1, checkpoint2, checkpoint3, checkpoint4, checkpoint5])

