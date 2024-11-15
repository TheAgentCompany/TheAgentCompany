from typing import List
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scoring import Result, Checkpoint, bonus_for_completing_any
from common import grader


@grader
def grade_checkpoint1(trajectory: str) -> bool:
    stock_test_answer = pd.read_csv('./splitted before/stock_test_answer_golden.csv')
    golden_answer = pd.read_csv('./splitted before/stock_test_answer.csv')

    actual, pred = stock_test_answer['Close Price'], golden_answer['Close Price']
    mse = mean_squared_error(actual, pred)
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    
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
    result = Result(checkpoints, bonus_for_completing_any)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    return result
