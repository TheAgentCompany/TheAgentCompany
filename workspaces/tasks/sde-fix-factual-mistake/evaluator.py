import logging
import os
import yaml
from common import *


# Check if OpenHands repo is cloned
def grade_checkpoint1():
    return check_repo_exists('openhands')

# Check L20 is fixed to be Thursday instead of Saturday
def grade_checkpoint2():
    yaml_path = '/workspace/openhands/agenthub/micro/math_agent/agent.yaml'
    try:
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)
        
        examples = data.get('examples', [])
        for example in examples:
            if example.get('inputs', {}).get('task') == "What day of the week is 2099-01-01?":
                return example.get('outputs', {}).get('answer') == "Thursday"
        
        logging.warning("No relevant example found for checkpoint 2")
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint2: {e}")
        return False

# Check L24 is fixed to be close to 0.620537 instead of 0.603848
def grade_checkpoint3():
    yaml_path = '/workspace/openhands/agenthub/micro/math_agent/agent.yaml'
    try:
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)
        
        examples = data.get('examples', [])
        for example in examples:
            if example.get('inputs', {}).get('task') == "What is the integral of sin(x^2) evaluated from -1 to 1?":
                answer = example.get('outputs', {}).get('answer')
                try:
                    value = float(answer)
                    return abs(value - 0.620537) < 0.001
                except ValueError:
                    logging.warning("Invalid float value for integral answer")
                    return False
        
        logging.warning("No relevant example found for checkpoint 3")
        return False
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint3: {e}")
        return False

def grade_checkpoint(check_func, description):
    try:
        passed = check_func()
        print(f"{'✓' if passed else '✗'} {description}")
        return 1 if passed else 0
    except Exception as e:
        logging.warning(f"Error while grading checkpoint '{description}': {e}")
        return 0

if __name__ == "__main__":
    checkpoints = [
        (grade_checkpoint1, "OpenHands repo is cloned"),
        (grade_checkpoint2, "L20 is fixed to be Thursday instead of Saturday"),
        (grade_checkpoint3, "L24 is fixed to be close to 0.620537 instead of 0.603848"),
    ]

    points = 0
    for check_func, description in checkpoints:
        point = grade_checkpoint(check_func, description)
        points += point 
        

    print(f"\nFinal points for OpenHands task: {points}/3")