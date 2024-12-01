from typing import List
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scoring import Result, Checkpoint
from common import grader, check_file_in_owncloud_directory, get_binary_file_content_owncloud
from io import BytesIO
import logging

@grader
def grade_checkpoint1():
    file_name = "stock_test_answer.csv"
    dir_name = "Documents/Financials"
    if not check_file_in_owncloud_directory(file_name, dir_name):
        return 0

    content = get_binary_file_content_owncloud(file_name, dir_name)
    if not content:
        logging.warning("Failed to download content {file_name}")
        return 0

    try:
        stock_test_answer = pd.read_csv(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read {file_name}: {e}")
        return 0
    
    golden_answer = pd.read_csv('/utils/golden_answer.csv')

    actual, pred = golden_answer['Close Price'], stock_test_answer['Close Price']
    mse = mean_squared_error(actual, pred)
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)

    logging.info(f'On private test dataset, MSE: {mse}, MAE: {mae}, R^2: {r2}')
    
    # 3 credit granted if MSE < 500, MAE < 10, R^2 score > 0.8
    if mse < 500 and mae < 10 and r2 > 0.8:
        return 3
    # 2 credits granted if MSE < 550, MAE < 20, R^2 score > 0.7
    elif mse < 550 and mae < 20 and r2 > 0.7:
        return 2
    # No credits granted if MSE > 550, MAE > 20, R^2 score < 0.7
    else:
        return 0


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(3, int(grade_checkpoint1())))

    return result
