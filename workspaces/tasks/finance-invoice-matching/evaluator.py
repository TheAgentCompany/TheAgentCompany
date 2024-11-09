import pandas as pd
import logging
from typing import List

from common import check_file_in_nextcloud_directory, download_nextcloud_content
from scoring import Result, Checkpoint, bonus_for_completing_any
from config import NEXTCLOUD_URL


def grade_checkpoint1(trajectory):
    urls = [f"{NEXTCLOUD_URL}/apps/files/files/1421?dir=/Documents/Financials/payments.xlsx&openfile=true", f"{NEXTCLOUD_URL}/apps/files/files/1422?dir=/Documents/Financials/invoices_pdfs"]
            
    return all(url in trajectory for url in urls)

def grade_checkpoint2():
    file_name = "flagged_payments.xlsx"
    dir_name = "Documents/Financials"
    if not check_file_in_nextcloud_directory(file_name, dir_name):
        return False

    if not download_nextcloud_content("{NEXTCLOUD_URL}/apps/files/files/1421?dir=/Documents/Financials/flagged_payments.xlsx", "/workspace/downloaded.md"):
        logging.warning("Failed to download content")
        return False
    
    flagged_df = pd.read_excel('/workspace/invoice_matching.xlsx')

    required_columns = ["Payment_ID", "Issue"]
    if not all(column in flagged_df.columns for column in required_columns):
        return False

    # Check if the last row follows the specified format
    last_row = flagged_df.iloc[-1]
    if (
        last_row["Payment_ID"] == "TOTAL"
        and "Total amount mismatch" in last_row["Issue"]
    ):
        return True
    else:
        return False
    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))

    return result

