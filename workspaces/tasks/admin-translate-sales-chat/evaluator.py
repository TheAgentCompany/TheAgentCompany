import re

import logging
from typing import List

from scoring import Result, Checkpoint


def grade_checkpoints(trajectory=""):
    # reference answer's detailed computation is documented in README.md
    REFERENCE_ANSWER = 145095

    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    total_score = 4
    try:
        with open('/workspace/ans.txt', 'r') as file:
            content = file.read().strip()
            
            # Use regex to find all numbers in the content
            numbers = re.findall(r'\b\d*\.?\d+(?:[eE][-+]?\d+)?\b', content)
            
            # Check if there's exactly one number
            if len(numbers) != 1:
                checkpoints.append(Checkpoint(total_score, 0))
            else: 
                number = int(numbers[0])
                if abs(number - REFERENCE_ANSWER) / float(REFERENCE_ANSWER) <= 0.02:
                    checkpoints.append(Checkpoint(total_score, 4))
                elif abs(number - REFERENCE_ANSWER) / float(REFERENCE_ANSWER) <= 0.1:
                    checkpoints.append(Checkpoint(total_score, 2))
                else:
                    checkpoints.append(Checkpoint(total_score, 0))
    except FileNotFoundError:
        logging.warning("/workspace/ans.txt is not found")
        checkpoints.append(Checkpoint(total_score, 0))

    return result


