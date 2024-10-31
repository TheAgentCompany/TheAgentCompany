"""Summary of evaluator for example task

You don't have to write a summary for the evaluator, although documentation is
strongly encouraged.

A good evaluator should:
1. be robust - it shouldn't abort because of its own bug or lack of fail over mechanism
2. be deterministic and idempotent
3. grant partial credits if possible
4. encourage but not require trajectory for grading
"""

import os
import requests
import pandas as pd

from typing import List
from scoring import Result, Checkpoint, bonus_for_completing_final
from common import create_rocketchat_client, get_chat_history

rocket = create_rocketchat_client()


def grade_checkpoint1():
    chat = get_chat_history(rocket, "Huang Jie")
    return len(chat) > 0


def grade_checkpoint2():
    return os.path.exists('/workspace/meeting_feedback.xlsx')


def grade_checkpoint3():
    df = pd.read_excel("/workspace/meeting_feedback.xlsx")
    return sorted(df["Name"].tolist()) == ['Chen Xinyi', 'Emily Zhou', 'Huang Jie', 'Liu Qiang', 'Mike Chen']


def grade_checkpoint4():
    df = pd.read_excel("/workspace/meeting_feedback.xlsx")
    row = df[df["Name"]=="Chen Xinyi"]
    return (pd.isna(row["Score"]).tolist()[0]) and (pd.isna(row["Feedback"]).tolist()[0])

def grade_checkpoint5():
    df = pd.read_excel("/workspace/meeting_feedback.xlsx")
    others_df = df[df["Name"] != "Chen Xinyi"]
    others_feedback = others_df["Feedback"].tolist()
    if not all(["helpful" in feedback for feedback in others_feedback]):
        return False
    others_scores = others_df["Score"].tolist()
    if min(others_scores) < 4:
        return False
    return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))
    
    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(1, int(passed4)))

    passed5 = grade_checkpoint5()
    checkpoints.append(Checkpoint(1, int(passed5)))

    return result
