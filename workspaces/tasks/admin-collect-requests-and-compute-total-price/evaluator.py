import json
import logging

from common import *
from scoring import Checkpoint, Result
from typing import List

rocket = create_rocketchat_client()
 

def checkpoint1():
    passed = True
    for name in ['huang_jie', 'sophia_rodriguez', 'mike_chen', 'sarah_johnson']:
        passed = passed and get_chat_history(rocket, name)
    return passed

def checkpoint2(trajectory):
    return "apps/files/files/1351?dir=/Documents/Administrative%20Specialist&openfile=true" in trajectory

def checkpoint3(filepath):
    """
    Huang Jie one Monitor (27” Dell UltraSharp 4K cost $1799 and two External Hard Drive (2TB) cost $129 each, total cost $1799 + 2*$129 = $2057
    Sophia Rodriguez five Printer Paper (5000 sheets) cost $45 and four Notebooks (Pack of 5) cost $25 each, total cost $45*5 + $25*4 = $325
    Mike Chen apply one Ergonomic Office Chai cost $1195 and one Desk Lamp cost $49, total cost $1195 + $49 = $1244
    Sarah Johnson one Coffee Machine cost $299, one Microwave cost $129, one Mini Fridge cost $199 and one Water Dispenser cost $249, total cost $299 + $129 + $199 + $249 = $876

    four people's total cost = $2057 + $325 + $1244 + $876 = $4502
    """
    try:
        with open(filepath, 'r') as f:
            result = f.read()
    except Exception as e:
        logging.error(f"Error processing file {filepath}: {e}")
        return False
    return '4502' in result

def grade_checkpoints(trajectory=''):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = checkpoint2(trajectory)
    checkpoints.append(Checkpoint(1, 1 * int(passed2)))

    passed3 = checkpoint3(filepath='result.txt')
    checkpoints.append(Checkpoint(1, 1 * int(passed3)))

    return result

