import re
import json
import logging

def grade_checkpoints(trajectory):
    # reference answer's detailed computation is documented in README.md
    REFERENCE_ANSWER = 145095

    result = {'final_score': 0}

    try:
        with open('/workspace/ans.txt', 'r') as file:
            content = file.read().strip()
            
            # Use regex to find all numbers in the content
            numbers = re.findall(r'\b\d*\.?\d+(?:[eE][-+]?\d+)?\b', content)
            
            # Check if there's exactly one number
            if len(numbers) != 1:
                return result
            
            number = int(numbers[0])
            
            if abs(number - REFERENCE_ANSWER) / float(REFERENCE_ANSWER) <= 0.02:
                result['final_score'] = 4
            elif abs(number - REFERENCE_ANSWER) / float(REFERENCE_ANSWER) <= 0.1:
                result['final_score'] = 2
            else:
                result['final_score'] = 0
    except FileNotFoundError:
        logging.warning("/workspace/ans.txt is not found")
    return result

if __name__ == "__main__":
    print(json.dumps(grade_checkpoints()))
