import csv
import json
import logging
from collections import defaultdict
from typing import List

from scoring import Result, Checkpoint

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    drinks_count = defaultdict(int)

    try:
        with open('/workspace/drinks_survey.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                drink = row['drink'].strip().lower()
                quantity = int(row['quantity'])
                drinks_count[drink] += quantity
    except FileNotFoundError:
        logging.error("File '/workspace/drinks_survey.csv' not found")
    except csv.Error:
        logging.error("Unable to parse the CSV file. Make sure it's properly formatted.")
    except ValueError:
        logging.error("Invalid quantity value in the CSV. All quantities should be integers.")

    # Checkpoint 1
    unique_drinks = set(drinks_count.keys())
    if len(unique_drinks) == 9:
        logging.info("Checkpoint 1: Correct! There are 9 unique drinks. (2 points)")
        checkpoints.append(Checkpoint(2, 2))
    elif len(unique_drinks) == 8:
        logging.warning("Checkpoint 1: Close! You found 8 unique drinks. Did you notice 'diet coke'? (1 point)")
        checkpoints.append(Checkpoint(2, 1))
    else:
        logging.warning(f"Checkpoint 1: Incorrect. You found {len(unique_drinks)} unique drinks. Check for 'diet coke' and other variations. (0 points)")
        checkpoints.append(Checkpoint(2, 0))

    # Checkpoint 2
    apple_juice_count = drinks_count['apple juice']
    if apple_juice_count == 4:
        logging.info("Checkpoint 2: Correct! There are 4 Apple Juice entries. (1 point)")
        checkpoints.append(Checkpoint(1, 1))
    else:
        logging.warning(f"Checkpoint 2: Incorrect. You counted {apple_juice_count} Apple Juice entries, but there should be 4. (0 points)")
        checkpoints.append(Checkpoint(1, 0))

    # Checkpoint 3
    required_drinks = {'vita coco', 'talking rain', 'milk'}
    if required_drinks.issubset(unique_drinks):
        logging.info("Checkpoint 3: Correct! Vita Coco, Talking Rain, and Milk are all present. (1 point)")
        checkpoints.append(Checkpoint(1, 1))
    else:
        missing = required_drinks - unique_drinks
        logging.warning(f"Checkpoint 3: Incorrect. Missing drinks: {', '.join(missing)}. (0 points)")
        checkpoints.append(Checkpoint(1, 0))

    # Checkpoint 4
    vita_coco_count = drinks_count['vita coco']
    if vita_coco_count == 2:
        logging.info("Checkpoint 4: Correct! The demand for Vita Coco is 2. (1 point)")
        checkpoints.append(Checkpoint(1, 1))
    else:
        logging.warning(f"Checkpoint 4: Incorrect. You counted {vita_coco_count} for Vita Coco, but it should be 2. (0 points)")
        checkpoints.append(Checkpoint(1, 0))

    return result

if __name__ == "__main__":
    print(json.dumps(grade_checkpoints().to_dict()))