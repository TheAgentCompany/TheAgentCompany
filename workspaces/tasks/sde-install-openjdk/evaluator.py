import shutil
import subprocess
import logging

# OpenJDK is installed
def grade_checkpoint1():
    try:
        output = run_command(["java", "--version"])
        return output is not None and "openjdk" in output.lower()
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 1: {e}")
        return False

# OpenJDK 17 is installed
def grade_checkpoint2():
    try:
        output = run_command(["java", "--version"])
        return output is not None and "openjdk 17." in output.lower()
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 2: {e}")
        return False

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
        (grade_checkpoint1, "OpenJDK is installed (java --version returns 'openjdk xxx')"),
        (grade_checkpoint2, "OpenJDK 17 is installed (openjdk 17.xx keyword is in it)"),
    ]

    points = 0
    for check_func, description in checkpoints:
        point = grade_checkpoint(check_func, description)
        points += point
        if point == 0:
            break

    print(f"\nFinal points for OpenJDK installation task: {points}/2")