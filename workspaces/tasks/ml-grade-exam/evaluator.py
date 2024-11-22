import requests
import os
import logging
from datetime import datetime, timezone
from typing import List
import json

from scoring import Result, Checkpoint
from config import *
from common import *

############################# init variable #####################################


############################# helper functions #####################################

############################# grade checkpoints #####################################

@grader
def grade_checkpoint1():
    base_name = 'AgentCompany_ML_Quiz_Attempt'
    files_found = {f'{base_name}{i}':False for i in range(1,7)}

    for file in os.listdir('/workspace'):
        file_prefix = file[:len(base_name)+1] if len(file)>=len(base_name)+1 else ''
        if file_prefix in files_found:
            files_found[file_prefix] = True

    for key in files_found:
        if not files_found[key]:
            logging.warning(f'File starting with {key} not found')
            return False

    return True

@grader
def grade_checkpoint2(project_id, all_issues):
    base_name = 'AgentCompany_ML_Quiz_Attempt'
    files_graded = {
        'AgentCompany_ML_Quiz_Attempt1_1':False,
        'AgentCompany_ML_Quiz_Attempt2_15':False,
        'AgentCompany_ML_Quiz_Attempt3_9':False,
        'AgentCompany_ML_Quiz_Attempt4_12':False,
        'AgentCompany_ML_Quiz_Attempt5_11':False,
        'AgentCompany_ML_Quiz_Attempt6_10':False
    }

    for file in os.listdir('/workspace'):
        file_prefix = file.split('.')[0].split('-')[0]
        if file_prefix in files_graded:
            files_graded[file_prefix] = True

    score = 0

    for key in files_graded:
        if not files_graded[key]:
            logging.warning(f'File starting with {key[:len(base_name)+1]} not graded correctly')
        else:
            score+=1

    return score

@grader
def grade_checkpoint3(next_cycle_issues):
    for file in os.listdir('/workspace'):
        #Check if wrong file or multiple files are selected for submission
        if 'submit' in file and file != 'AgentCompany_ML_Quiz_Attempt2_15-submit.pdf':
            return False

    #Check if correct file is picked for submission
    if not 'AgentCompany_ML_Quiz_Attempt2_15-submit.pdf' in os.listdir('/workspace'):
        return False

    return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(6, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))

    return result
