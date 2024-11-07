import logging
import re
from typing import List
from scoring import Result, Checkpoint
from common import *

# Expected results for validation
expected_results = {
    "task1": 20,  # Total number of products
    "task2": 3,   # Number of categories
    "task3": [    # Top 3 most expensive electronics
        ("Gaming Laptop G1", 1799.99),
        ("Professional Laptop T1", 1299.99),
        ("Tablet Pro T1", 899.99)
    ]
}

# Read each task's result file
def read_file_content(task_number):
    try:
        with open(f'task{task_number}.txt', 'r') as f:
            content = f.read().strip()
        return content
    except Exception as e:
        logging.warning(f"Error reading task{task_number}.txt: {e}")
        return None

# Parse the content of task3.txt into a list of tuples
def parse_task3_content(content):
    try:
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        results = []
        
        for line in lines:
            # Extract product name and price
            match = re.match(r'"([^"]+)"\s*,\s*([\d.]+)', line)
            if match:
                name = match.group(1)
                price = float(match.group(2))
                results.append((name, price))
                
        return results
    except Exception as e:
        logging.warning(f"Error parsing task3 content: {e}")
        return []

# Check if the total number of products matches
def grade_checkpoint1():
    content = read_file_content(1)
    try:
        if content is not None:
            return int(content.strip()) == expected_results["task1"]
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

# Check if the number of categories matches
def grade_checkpoint2():
    content = read_file_content(2)
    try:
        if content is not None:
            return int(content.strip()) == expected_results["task2"]
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False

# Check if the top 3 expensive electronics match
def grade_checkpoint3():
    content = read_file_content(3)
    try:
        if content is not None:
            results = parse_task3_content(content)
            if len(results) != 3:
                return False
            
            # Compare with expected results
            for actual, expected in zip(results, expected_results["task3"]):
                if actual[0] != expected[0] or abs(actual[1] - expected[1]) > 0.01:
                    return False
            return True
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint2()) * 2))
    checkpoints.append(Checkpoint(3, int(grade_checkpoint3()) * 3))
    
    return result