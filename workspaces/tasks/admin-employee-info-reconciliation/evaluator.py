import os
import logging
from typing import List

import pandas as pd

from scoring import Result, Checkpoint
from common import create_rocketchat_client, num_rocketchat_users_contacted, grader

rocket_client = create_rocketchat_client()


def load_employees_csv():
    if not os.path.exists('/workspace/employees.csv'):
        logging.error('employees.csv is not found')
        return None

    try:
        return pd.read_csv('/workspace/employees.csv')
    except Exception as e:
        logging.error(f'Error loading employees.csv: {e}')
        return None


@grader
def grade_checkpoint_1() -> bool:
    return num_rocketchat_users_contacted(rocket_client, ['priya_sharma', 'sophia_rodriguez', 'zhang_wei'])


@grader
def grade_checkpoint_2() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False

    try:
        return 'Chen Xinyi' in csv['name'].values
    except Exception as e:
        logging.error(f'Error checking Chen Xinyi: {e}')
        return False


@grader
def grade_checkpoint_3() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False

    try:
        if 'Priya Sharma' not in csv['name'].values:
            return False
        return csv.loc[csv['name'] == 'Priya Sharma', 'email'].values[0] == 'priyasharma@example.com' and \
               csv.loc[csv['name'] == 'Priya Sharma', 'phone'].values[0] == '516-837-4592'
    except Exception as e:
        logging.error(f'Error checking Priya Sharma: {e}')
        return False


@grader
def grade_checkpoint_4() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False

    try:
        if 'Sophia Rodriguez' not in csv['name'].values:
            return False
        return csv.loc[csv['name'] == 'Sophia Rodriguez', 'phone'].values[0] == '858-624-7193'
    except Exception as e:
        logging.error(f'Error checking Sophia Rodriguez: {e}')
        return False


@grader
def grade_checkpoint_5() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False

    try:
        if 'Zhang Wei' not in csv['name'].values:
            return False
        return csv.loc[csv['name'] == 'Zhang Wei', 'phone'].values[0] == '425-967-3841'
    except Exception as e:
        logging.error(f'Error checking Zhang Wei: {e}')
        return False


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(3, int(grade_checkpoint_1())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_2())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_3())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_4())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_5())))

    return result
