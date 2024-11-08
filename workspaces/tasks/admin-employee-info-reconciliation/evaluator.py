import os
import logging
from typing import List

import pandas as pd

from scoring import Result, Checkpoint
from common import create_rocketchat_client, num_rocketchat_users_contacted

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


def grade_checkpoint_1() -> bool:
    return num_rocketchat_users_contacted(rocket_client, ['Priya Sharma', 'Sophia Rodriguez', 'Zhang Wei']) == 3


def grade_checkpoint_2() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False
    return 'Chen Xinyi' in csv['Name'].values


def grade_checkpoint_3() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False
    if 'Priya Sharma' not in csv['Name'].values:
        return False
    return csv.loc[csv['Name'] == 'Priya Sharma', 'Email'].values[0] == 'priyasharma@example.com' and \
           csv.loc[csv['Name'] == 'Priya Sharma', 'Phone'].values[0] == '516-837-4592'


def grade_checkpoint_4() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False
    if 'Sophia Rodriguez' not in csv['Name'].values:
        return False
    return csv.loc[csv['Name'] == 'Sophia Rodriguez', 'Phone'].values[0] == '858-624-7193'


def grade_checkpoint_5() -> bool:
    csv = load_employees_csv()
    if csv is None:
        return False
    if 'Zhang Wei' not in csv['Name'].values:
        return False
    return csv.loc[csv['Name'] == 'Zhang Wei', 'Phone'].values[0] == '425-967-3841'


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_1())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_2())))

    checkpoints.append(Checkpoint(3, int(grade_checkpoint_3())))

    checkpoints.append(Checkpoint(4, int(grade_checkpoint_4())))

    checkpoints.append(Checkpoint(5, int(grade_checkpoint_5())))

    return result
