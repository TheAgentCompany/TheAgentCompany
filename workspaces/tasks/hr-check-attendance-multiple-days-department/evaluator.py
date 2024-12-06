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


def parse_department_data(filename):
    data = {
        "Department": [],
        "Name": []
    }

    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip().strip('\n')
            department, names = line.split(':')
            department = department.replace('•', '').strip()
            names_list = [name.strip() for name in names.split(',')]

            data["Department"].extend([department] * len(names_list))
            data["Name"].extend(names_list)
    return pd.DataFrame(data)


def compare_row_by_row(output_df, correct_df):
    expected_cols_name = ["departmentaverageworklength", "departmentaverageontimedeparturecount", "departmentaveragelatearrivalcount"]
    for department_name in output_df["department"].to_list():
        answer_row = output_df[output_df['department'] == department_name]
        expected_row = correct_df[correct_df['department'] == department_name]
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


def merge_department_with_employee_df(department_df, employee_df):
    return pd.merge(employee_df, department_df, on="Name", how="left")


def aggregate_by_department(merged_df):
    aggregated_df = merged_df.groupby("Department").agg({
        "Average Work Length": "mean",  
        "On-time Departure Count": "mean",
        "Late Arrival Count": "mean",
        }).reset_index()
    aggregated_df.rename(columns={
        "Average Work Length": "Department Average Work Length",
        "On-time Departure Count": "Department Average On-time Departure Count",
        "Late Arrival Count": "Department Average Late Arrival Count"
    }, inplace=True)
    return aggregated_df


def standardize_df(df):
    if df is None:
        return None
    df.columns = df.columns.str.replace(' ', '').str.lower().str.replace('-', '')
    if "department" in df.columns:
        df = df.sort_values(by="department").reset_index(drop=True)
    return df


@grader
def grade_checkpoint1():
    if not check_excel_file_exists("/workspace/department-april-attendance.xlsx"):
        return False
    try:
        df = standardize_df(pd.read_excel("/workspace/department-april-attendance.xlsx"))
        return set(df.columns).issuperset(set(["department", "departmentaverageworklength", "departmentaverageontimedeparturecount", "departmentaveragelatearrivalcount"]))
    except Exception:
        return False


@grader
def grade_checkpoint2():
    agent_output = standardize_df(read_excel("/workspace/department-april-attendance.xlsx"))

    department_df = parse_department_data('/utils/department.txt')
    employee_df = analyze_csv('/utils/april-attendance-data.csv')
    merge_expected_df = standardize_df(aggregate_by_department(merge_department_with_employee_df(department_df=department_df, employee_df=employee_df)))
    if agent_output is None or merge_expected_df is None:
        return False
    try:
        if set(agent_output["department"].to_list()) != set(merge_expected_df["department"].to_list()):
            return False
        return compare_row_by_row(agent_output, merge_expected_df)
    except Exception as e:
        return False


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(2, 2 * int(grade_checkpoint2())))
    return result
