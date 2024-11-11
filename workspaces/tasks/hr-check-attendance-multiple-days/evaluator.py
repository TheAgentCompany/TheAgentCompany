import os

from typing import List

import pandas as pd
from datetime import datetime

from scoring import Result, Checkpoint, bonus_for_completing_final
import logging
from common import grader


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
        return df
    except Exception:
        return None


def compare_row_by_row(output_df, correct_df):
    expected_cols_name = ["averageworklength", "on-timedeparturecount", "latearrivalcount"]
    for name in output_df["name"].to_list():
        answer_row = output_df[output_df['name'] == name]
        expected_row = correct_df[correct_df['name'] == name]
        for col in expected_cols_name:
            if not (abs(answer_row[col] - expected_row[col]) < 1e-5).item():
                return False
    return True


def analyze_csv(filename):
    try:
        df = pd.read_csv(filename)

        # Strip out the spaces if there are any
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        df['Clock-in'] = pd.to_datetime(df['Clock-in'], format='%H:%M').dt.time
        df['Clock-out'] = pd.to_datetime(df['Clock-out'], format='%H:%M').dt.time

        # Calculate work length in hours
        def work_length(row):
            clock_in = pd.Timestamp.combine(pd.Timestamp(row['Date']), row['Clock-in'])
            clock_out = pd.Timestamp.combine(pd.Timestamp(row['Date']), row['Clock-out'])
            return (clock_out - clock_in).seconds / 3600

        start_time = datetime.strptime("17:30", "%H:%M").time()
        end_time = datetime.strptime("18:00", "%H:%M").time()

        def is_ontime_departure(row):
            return row['Clock-out'] > start_time and row['Clock-out'] < end_time

        def is_late(row):
            return row['Clock-in'] > datetime.strptime("9:00", "%H:%M").time()

        df['Work Length'] = df.apply(work_length, axis=1)
        df['On-Time Departure'] = df.apply(is_ontime_departure, axis=1)
        df['Late Arrival'] = df.apply(is_late, axis=1)

        results = df.groupby('Name').agg(
            Average_Work_Length=('Work Length', 'mean'),
            Ontime_Departure=('On-Time Departure', 'sum'),
            Late_Arrival=('Late Arrival', 'sum')
        ).reset_index()

        results.columns = ['Name', 'Average Work Length', 'On-time Departure Count', 'Late Arrival Count']
        return results
    except Exception:
        return None


@grader
def grade_checkpoint1(trajectory):
    urls = [f"/apps/files/files/1233?dir=/Documents/Human%20Resources%20Team/Attendance"]
    return any(url in trajectory for url in urls)


@grader
def grade_checkpoint2():
    if not check_excel_file_exists("/workspace/april-attendance.xlsx"):
        return False
    try:
        df = standardize_df(pd.read_excel("/workspace/april-attendance.xlsx"))
        return set(df.columns).issuperset(set(["name", "averageworklength", "on-timedeparturecount", "latearrivalcount"]))
    except Exception:
        return False


def standardize_df(df):
    if df is None:
        return None
    df.columns = df.columns.str.replace(' ', '').str.lower()
    df = df.sort_values(by="name").reset_index(drop=True)
    return df


@grader
def grade_checkpoint3():
    output = standardize_df(read_excel("/workspace/april-attendance.xlsx"))
    expected_answer = standardize_df(analyze_csv('/utils/april-attendance-data.csv'))
    if output is None or expected_answer is None:
        return False
    if set(output["name"].to_list()) != set(expected_answer["name"].to_list()):
        return False
    return compare_row_by_row(output, expected_answer)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    return result
