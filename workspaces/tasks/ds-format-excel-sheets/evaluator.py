import logging
import os
import subprocess
from sotopia.database import AgentProfile

from typing import List

from scoring import Result, Checkpoint
from common import *

def grade_checkpoint1():
    try:
        result = subprocess.run(['curl', '-I', 'https://nextcloud.example.com/s/your-file-link'], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("Agent visited the file link on NextCloud.")
            return True
        else:
            logging.warning("Agent did not visit the file link on NextCloud.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the file link on NextCloud: {e}")
        return False

def grade_checkpoint2():
    try:
        import pandas as pd

        file_path = '/workspace/sotopia/data/your_excel_file.xlsx'
        if not os.path.exists(file_path):
            logging.warning("Excel file not found in the data folder.")
            return False

        df = pd.read_excel(file_path, sheet_name='unformatted')
        if df.equals(pd.read_excel(file_path, sheet_name='unformatted')):
            logging.info("The 'unformatted' sheet remains unchanged.")
            return True
        else:
            logging.warning("The 'unformatted' sheet has been changed.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the 'unformatted' sheet: {e}")
        return False

def grade_checkpoint3():
    try:
        import pandas as pd

        file_path = '/workspace/sotopia/data/your_excel_file.xlsx'
        if not os.path.exists(file_path):
            logging.warning("Excel file not found in the data folder.")
            return False

        xls = pd.ExcelFile(file_path)
        if 'formatted' in xls.sheet_names:
            logging.info("The 'formatted' sheet is created.")
            return True
        else:
            logging.warning("The 'formatted' sheet is not created.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the 'formatted' sheet: {e}")
        return False

def grade_checkpoint4():
    try:
        import pandas as pd

        file_path = '/workspace/sotopia/data/your_excel_file.xlsx'
        if not os.path.exists(file_path):
            logging.warning("Excel file not found in the data folder.")
            return False

        df = pd.read_excel(file_path, sheet_name='formatted')
        # Add your specific formatting checks here
        if df['column_name'].dtype == 'desired_dtype':  # Example check
            logging.info("The required formatting changes are applied.")
            return True
        else:
            logging.warning("The required formatting changes are not applied.")
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking the formatting changes: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    # Checkpoint 1: Agent visited the file link on NextCloud
    passed_checkpoint1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed_checkpoint1)))

    # Checkpoint 2: The 'unformatted' sheet remains unchanged
    passed_checkpoint2 = passed_checkpoint1 and grade_checkpoint2()
    checkpoints.append(Checkpoint(2, int(passed_checkpoint2)))

    # Checkpoint 3: The 'formatted' sheet is created
    passed_checkpoint3 = passed_checkpoint2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(3, int(passed_checkpoint3)))

    # Checkpoint 4: The required formatting changes are applied
    passed_checkpoint4 = passed_checkpoint3 and grade_checkpoint4()
    checkpoints.append(Checkpoint(4, 2 * int(passed_checkpoint4)))

    return result



