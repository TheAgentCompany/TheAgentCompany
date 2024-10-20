import shutil
import subprocess
import logging
import time
from subprocess import DEVNULL

def run_command(command):
    if not shutil.which(command[0]):
        logging.warning(f"Command '{command[0]}' not found in PATH")
        return None
    try:
        result = subprocess.run(command, check=False, timeout=0.1, stdout=DEVNULL)
        if result.returncode != 0:
            logging.warning(f"Command '{' '.join(command)}' failed with return code {result.returncode}")
            return None
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print("Successfully terminated after 0.1 second. No need to run indefinitely for testing")
        return True
    except Exception as e:
        print(type(e))
        logging.error(f"Error running command '{' '.join(command)}': {e}")
        return None


def grade_checkpoint1():
    try:
        output = run_command(["/workspace/risingwave"])
        return output is not None
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 1: {e}")
        return False


def grade_checkpoint2():
    try:
        p = subprocess.Popen(["/workspace/risingwave"], stdout=DEVNULL)
        time.sleep(12)
        pipe = subprocess.run(['psql', '-h', 'localhost', '-p', '4566', '-d' ,'dev', '-U','root', '-c', "SELECT * FROM average_exam_scores"], stdout=subprocess.PIPE)
        print("---------QUERY OUTPUT---------")
        output = pipe.stdout.decode('utf-8')
        print(output)
    except Exception as e:
        logging.error(f"Fail to grade checkpoint 2: {e}")
        p.terminate()
        return p, False
    else:
        p.terminate()
        return p, all(item in output for item in ["exam_id", "average_score", "total_scores", "101", "102", "87.74", "88.64", "5"])
    

if __name__ == "__main__":
    points = 0

    if grade_checkpoint1():
        points += 1
    
    process, res = grade_checkpoint2()
    if res:
        points += 1

    process.wait()

    print(f"\nFinal points for running Rising Wave locally: {points}/2")