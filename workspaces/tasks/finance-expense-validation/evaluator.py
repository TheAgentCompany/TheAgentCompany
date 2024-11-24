import os
import pandas as pd
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
import logging
from common import grader

def check_file_exists(file_path):
    abs_path = os.path.abspath(file_path)
    try:
        return os.path.isfile(abs_path)
    except Exception as e:
        logging.warning(f"Error in check_file_exists: {e}")
        return False

@grader
def grade_checkpoint1(trajectory):
    """
    Check if the trajectory includes the correct owncloud file path.
    """
    expected_path = "Documents/Financials/Expenses"
    return expected_path in trajectory

@grader
def grade_checkpoint2():
    """
    Verify that the corrected expenses match the expenses_corrected file.
    """
    if not check_file_exists("/workspace/expenses_corrected.xlsx"):
        return False
    try:
        corrected_df = pd.read_excel("/workspace/expenses_corrected.xlsx")
        # Assuming a reference solution is available for comparison
        reference_df = pd.read_excel("/utils/ref_expenses_corrected.xlsx")
        return corrected_df.equals(reference_df)
    except Exception:
        return False

@grader
def grade_checkpoint3():
    """
    Verify the structure of the expense analysis report.
    """
    if not check_file_exists("/workspace/expenses_analysis.csv"):
        return False
    try:
        analysis_df = pd.read_csv("/workspace/expenses_analysis.csv")
        expected_columns = {"Correct_Category", "Total_Amount", "Number_of_Employees", "Cost_Per_Employee"}
        return set(analysis_df.columns) == expected_columns
    except Exception:
        return False

@grader
def grade_checkpoint4():
    """
    Verify the calculations and values in the expense analysis report.
    """
    if not check_file_exists("/workspace/expenses_analysis.csv"):
        return False
    try:
        analysis_df = pd.read_csv("/workspace/expenses_analysis.csv")
        # Assuming a reference solution is available for comparison
        reference_analysis_df = pd.read_csv("/utils/ref_expenses_analysis.csv")
        return analysis_df.equals(reference_analysis_df)
    except Exception:
        return False

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(2, grade_checkpoint2()))
    checkpoints.append(Checkpoint(3, grade_checkpoint3()))
    checkpoints.append(Checkpoint(4, grade_checkpoint4()))
    return result

