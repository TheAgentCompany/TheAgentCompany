import os

from typing import List

import pandas as pd

from scoring import Result, Checkpoint, bonus_for_completing_final
import logging
import math
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


def parse_rates_data(filename):
    data = {
        "Rate": [],
        "Name": []
    }

    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip().strip('\n')
            name, rate = line.split(':')
            name = name.strip()
            rate = float(rate.strip())
            data["Rate"].append(rate)
            data["Name"].append(name)
    return pd.DataFrame(data)


def compare_row_by_row(output_df, correct_df):
    expected_cols_name = ["totalearnings"]
    for name in output_df["name"].to_list():
        answer_row = output_df[output_df['name'] == name]
        expected_row = correct_df[correct_df['name'] == name]
        for col in expected_cols_name:
            if not (abs(answer_row[col] - expected_row[col]) < 1e-2).item():
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

        df['Work Length'] = df.apply(work_length, axis=1)

        results = df.groupby('Name').agg(
            total_work_length=('Work Length', 'sum'),
        ).reset_index()

        # Round up the final hours. There could be some significant discrepency in final
        # earnings calculation depending on how the intermediate work hours are rounded, especially since 
        # the hourly rate can be a large number. Rounding up the final hours should eliminate this issue. 
        results['total_work_length'] = results['total_work_length'].apply(math.ceil)

        results.columns = ['Name', 'Total Work Length']
        return results
    except Exception:
        return None


def final_earnings_df(hourly_rate, employee_df):
    df = pd.merge(employee_df, hourly_rate, on="Name", how="left")
    df['Total Earnings'] = df['Total Work Length'] * df['Rate']
    df['Total Earnings'] = df['Total Earnings'].round(2)
    z= df[['Name', 'Total Earnings']]
    return z

@grader
def grade_checkpoint1(trajectory):
    urls = ["dir=/Documents/Human%20Resources%20Team/Attendance", "dir=/Documents/Human%20Resources%20Team/Attendance"]
    return all(url in trajectory for url in urls)


@grader
def grade_checkpoint2():
    if not check_excel_file_exists("/workspace/april-payroll.xlsx"):
        return False
    try:
        df = standardize_df(pd.read_excel("/workspace/april-payroll.xlsx"))
        return set(df.columns).issuperset(set(["name", "totalearnings"]))
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
    output = standardize_df(read_excel("/workspace/april-payroll.xlsx"))

    rates_df = parse_rates_data('/utils/rates_info.txt')
    employee_df = analyze_csv('/utils/april-attendance-data.csv')
    expected_earnings = standardize_df(final_earnings_df(hourly_rate=rates_df, employee_df=employee_df))
    if output is None or expected_earnings is None:
        return False
    if set(output["name"].to_list()) != set(expected_earnings["name"].to_list()):
        return False
    return compare_row_by_row(output, expected_earnings)


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    return result
