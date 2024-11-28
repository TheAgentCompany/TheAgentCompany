import os
import pandas as pd
from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
import logging
from common import grader, evaluate_chat_history_with_llm, create_rocketchat_client

rocket = create_rocketchat_client()

REFERENCE_CONTRACTS = ["CTR006", "CTR037", "CTR069", "CTR080", 
                       "CTR093", "CTR103", "CTR118", "CTR135", 
                       "CTR138", "CTR143", "CTR183"]

REFERENCE_FLAGGED_FILE = '/workspace/flagged_contracts.xlsx'

REFERENCE_EMPLOYEES = ['David Wong', 'Jessica Lee', 'Li Ming', 'Priya Sharma']

@grader
def grade_checkpoint1(trajectory):
    """
    Check if the trajectory includes the correct owncloud file path.
    """
    expected_path = "Documents/Human%20Resources%20Team/Contracts"
    return expected_path in trajectory

@grader
def grade_checkpoint2():
    """
    Verify that the solution file is created.
    """
    if not os.path.exists(REFERENCE_FLAGGED_FILE):
        return False
    return True

@grader
def grade_checkpoint3():
    """
    Check that the flagged contracts match.
    """
    if not os.path.exists(REFERENCE_FLAGGED_FILE):
        return False

    flagged_df = pd.read_excel(REFERENCE_FLAGGED_FILE)
    flagged_contracts = flagged_df['Flagged_Contracts'].tolist()
    flagged_contracts_sorted = sorted(flagged_contracts)
    reference_contracts_sorted = sorted(REFERENCE_CONTRACTS)

    return flagged_contracts_sorted == reference_contracts_sorted

def grade_checkpoint4():
    """
    Contact the employees on RocketChat that have a flagged contract
    """
    predicate = "Person has been told that they have a flagged contract"
    for name in REFERENCE_EMPLOYEES:
        res = evaluate_chat_history_with_llm(rocket, name, predicate)
        if res == False:
            return False
    return True

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)
    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    checkpoints.append(Checkpoint(1, grade_checkpoint4()))
    return result
