import re
import logging
import json

def grade_checkpoints(trajectory=None):
    result = {'final_score': 0}
    try:
        with open('/workspace/ans.txt', 'r') as file:
            content = file.read().strip()
            
            # Use regex to find all numbers in the content
            numbers = re.findall(r'\b\d+\b', content)
            
            # Check if there's exactly one number
            if len(numbers) != 1:
                return result
            
            number = int(numbers[0])
            
            if number == 4:
                result['final_score'] = 2
            else:
                result['final_score'] = 0
    except FileNotFoundError:
        logging.error('/workspace/ans.txt is not found')

    return result


if __name__ == "__main__":
    print(json.dumps(grade_checkpoints()))