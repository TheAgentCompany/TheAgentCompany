import logging
import numpy as np
import pandas as pd

from common import grader
from scoring import Result, Checkpoint
from create_reference_solution import generate_commit_report

CSV_FILE = "/workspace/commit_report.csv"
REFERENCE_SOLUTION = '/workspace/reference_report.csv'

generate_commit_report()

def read_csv():
    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        logging.error("Error reading CSV file: %s", e)
        return None
    return df


def get_reference_usernames_and_repos():
    ref_df = pd.read_csv(REFERENCE_SOLUTION)
    reference_usernames = ref_df['user'].unique().tolist()
    reference_repos = ref_df.columns[2:].tolist()
    return reference_usernames, reference_repos

#check if all usernames are included
@grader
def grade_checkpoint1():
    df = read_csv()
    if df is None:
        return False
    unique_usernames = df['user'].unique().tolist()
    reference_usernames, _ = get_reference_usernames_and_repos()
    return set(unique_usernames) == set(reference_usernames)

#check if all repo names are included
@grader
def grade_checkpoint2():
    df = read_csv()
    if df is None:
        return False
    unique_repos = df.columns[2:].tolist()
    _, reference_repos = get_reference_usernames_and_repos()
    if reference_repos is None:
        return False
    return set(unique_repos) == set(reference_repos)

#check if dates are in the appropriate format
@grader
def grade_checkpoint3():
    df = read_csv()
    if df is None:
        return False
    expected_format="%Y/%m/%d"
    invalid_dates = df[~df['week'].apply(lambda x: pd.to_datetime(x, format=expected_format, errors='coerce')).notna()]
    return invalid_dates.empty, invalid_dates['week'].tolist()


#check if the final file matches the expected format exactly
@grader
def grade_checkpoint4():
    df = read_csv()
    ref_df = pd.read_csv(REFERENCE_SOLUTION)
    if df is None or ref_df is None:
        return False
    return df.equals(ref_df)

def grade_checkpoints(trajectory="") -> Result:
    checkpoint1 = Checkpoint(1, 1*int(grade_checkpoint1()))
    checkpoint2 = Checkpoint(1, 1*int(grade_checkpoint2()))
    checkpoint3 = Checkpoint(1, 1*int(grade_checkpoint3()))
    checkpoint4 = Checkpoint(3, 3*int(grade_checkpoint4()))
    return Result([checkpoint1, checkpoint2, checkpoint3, checkpoint4])

