import shutil
import subprocess
import logging

# Check if go is installed (go version returns "go version xxx")
def grade_checkpoint1():
    try:
        output = run_command(["go", "version"])
        return output is not None and output.startswith("go version")
    except Exception as e:
            logging.error(f"Fail to grade checkpoint 1: {e}")

# Check if go 1.17 is installed (1.17 keyword is in it)
def grade_checkpoint2():
    try:
        output = run_command(["go", "version"])
        return output is not None and "1.17" in output
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 2: {e}")

def run_command(command):
    if not shutil.which(command[0]):
        logging.warning(f"Command '{command[0]}' not found in PATH")
        return None
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            logging.warning(f"Command '{' '.join(command)}' failed with return code {result.returncode}")
            return None
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Error running command '{' '.join(command)}': {e}")
        return None

def grade_checkpoint(check_func, description):
    try:
        passed = check_func()
        print(f"{'✓' if passed else '✗'} {description}")
        return 1 if passed else 0
    except Exception as e:
        logging.error(f"Error while grading checkpoint '{description}': {e}")
        return 0
    
if __name__ == "__main__":
    checkpoints = [
        (grade_checkpoint1, "Go is installed"),
        (grade_checkpoint2, "Go 1.17 is installed"),
    ]

    points = 0
    for check_func, description in checkpoints:
        point = grade_checkpoint(check_func, description)
        points += point
        if point == 0:
            break

    print(f"\nFinal points for install go task: {points}/2")