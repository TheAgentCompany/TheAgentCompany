import re

def evaluate_task():
    try:
        with open('/workspace/ans.txt', 'r') as file:
            content = file.read().strip()
            
            # Use regex to find all numbers in the content
            numbers = re.findall(r'\b\d+\b', content)
            
            # Check if there's exactly one number
            if len(numbers) != 1:
                return 0
            
            number = int(numbers[0])
            
            if number == 4:
                return 2
            else:
                return 0
    
    except FileNotFoundError:
        return 0

if __name__ == "__main__":
    points = evaluate_task()
    print(f"Evaluation completed. Final score: {points}/2")
