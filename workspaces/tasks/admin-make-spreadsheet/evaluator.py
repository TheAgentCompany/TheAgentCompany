import csv
from collections import Counter

def grade_drinks_survey():
    score = 0
    feedback = []
    
    try:
        with open('/workspace/drinks_survey.csv', 'r') as file:
            reader = csv.DictReader(file)
            drinks = [row['drink'].strip().lower() for row in reader]
    except FileNotFoundError:
        return 0, ["Error: File '/workspace/drinks_survey.csv' not found."]
    except csv.Error:
        return 0, ["Error: Unable to parse the CSV file. Make sure it's properly formatted."]

    # Checkpoint 1
    unique_drinks = set(drinks)
    if len(unique_drinks) == 9:
        score += 2
        feedback.append("Checkpoint 1: Correct! There are 9 unique drinks. (2 points)")
    elif len(unique_drinks) == 8:
        score += 1
        feedback.append("Checkpoint 1: Close! You found 8 unique drinks. Did you notice 'diet coke'? (1 point)")
    else:
        feedback.append(f"Checkpoint 1: Incorrect. You found {len(unique_drinks)} unique drinks. Check for 'diet coke' and other variations. (0 points)")

    # Checkpoint 2
    apple_juice_count = drinks.count('apple juice')
    if apple_juice_count == 4:
        score += 1
        feedback.append("Checkpoint 2: Correct! There are 4 Apple Juice entries. (1 point)")
    else:
        feedback.append(f"Checkpoint 2: Incorrect. You counted {apple_juice_count} Apple Juice entries, but there should be 4. (0 points)")

    # Checkpoint 3
    required_drinks = {'vita coco', 'talking rain', 'milk'}
    if required_drinks.issubset(unique_drinks):
        score += 1
        feedback.append("Checkpoint 3: Correct! Vita Coco, Talking Rain, and Milk are all present. (1 point)")
    else:
        missing = required_drinks - unique_drinks
        feedback.append(f"Checkpoint 3: Incorrect. Missing drinks: {', '.join(missing)}. (0 points)")

    # Checkpoint 4
    vita_coco_count = drinks.count('vita coco')
    if vita_coco_count == 2:
        score += 1
        feedback.append("Checkpoint 4: Correct! The demand for Vita Coco is 2. (1 point)")
    else:
        feedback.append(f"Checkpoint 4: Incorrect. You counted {vita_coco_count} for Vita Coco, but it should be 2. (0 points)")

    return score, feedback

if __name__ == "__main__":
    score, feedback = grade_drinks_survey
    print(f"Evaluation completed. Final score: {score}/5")
    print(feedback)
