import re
import logging

from typing import List

from scoring import Result, Checkpoint

def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    total_score = 2
    try:
        with open('/workspace/ans.txt', 'r') as file:
            content = file.read().strip()
            
            # Use regex to find all numbers in the content
            numbers = re.findall(r'\b\d+\b', content)
            
            # Check if there's exactly one number
            if len(numbers) != 1:
                checkpoints.append(Checkpoint(total_score, 0))
            else:
                number = int(numbers[0])
                if number == 4:
                    checkpoints.append(Checkpoint(total_score, 2))
                else:
                    checkpoints.append(Checkpoint(total_score, 0))
    except FileNotFoundError:
        logging.warning('/workspace/ans.txt is not found')
        checkpoints.append(Checkpoint(total_score, 0))

    return result


