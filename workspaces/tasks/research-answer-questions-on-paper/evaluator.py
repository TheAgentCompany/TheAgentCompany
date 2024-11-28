import os
import logging
from typing import List

from scoring import Result, Checkpoint
from config import *
from common import *

############################# init variable #####################################
ANALYSIS_SHEET = 'noise_simulation_analysis_sheet.txt'
REFERENCE_ANSWERS = '/utils/answers.txt'
############################# helper functions #####################################


############################# grade checkpoints #####################################

@grader
def grade_checkpoint1():
    filenames=[
            'noise_simulation_paper.pdf',
            ANALYSIS_SHEET
        ]
    for filename in filenames:
        if not os.path.exists(os.path.join('/workspace',filename)):
            logging.warning(f'{filename} not downloaded')
            return False
    return True

@grader
def grade_checkpoint2():
    with open(REFERENCE_ANSWERS,'r') as f:
        ref_answers = [line.strip() for line in f]

    score = 0

    if not os.path.exists(os.path.join('/workspace',ANALYSIS_SHEET)):
        logging.warning('Analysis sheet does not exist in the workspace directory')
        return 0

    with open(os.path.join('/workspace',ANALYSIS_SHEET),'r') as f:
        for i, line in enumerate(f):
            qa_pair = line.split(':')
            if len(qa_pair)<2:
                logging.warning('Analysis sheet corrupted')
                return 0
            answer = qa_pair[1].strip().lower().replace("<answer here>","")
            score+= 1 if evaluate_with_llm(answer,ref_answers[i]) else 0
            logging.info(f'Question {qa_pair[0]}, Expected Answer: {ref_answers[i]}, Agent Answer: {answer}')

    return score


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(11, int(grade_checkpoint2())))

    return result
