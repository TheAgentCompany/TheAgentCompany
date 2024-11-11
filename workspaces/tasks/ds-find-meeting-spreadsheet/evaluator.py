import logging
import os

from typing import List

from scoring import Result, Checkpoint
from common import *

@checkpoint
def grade_checkpoint1():
    try:
        with open('/workspace/link.txt', 'r') as file:
            link = file.read().strip()
            if link is not None and "apps/files/files/1447?dir=/Documents/Data%20Analysis" in link:
                logging.info("Correct link found in link.txt.")
                return True
            else:
                logging.warning("Incorrect link found in link.txt.")
                return False
    except FileNotFoundError:
        logging.error("File link.txt not found.")
        return False
    except Exception as e:
        logging.error(f"Error occurred while checking link.txt: {e}")
        return False

@checkpoint
def grade_checkpoint2():
    try:
        if os.path.isfile('/workspace/Seed Area Estimates.xlsx'):
            logging.info("File 'Seed Area Estimates.xlsx' successfully downloaded.")
            return True
        else:
            logging.warning("File 'Seed Area Estimates.xlsx' not found.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the file: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: Clone the repository
    passed_checkpoint1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint1)))

    # Checkpoint 2: create branch
    passed_checkpoint2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint2)))

    return result


