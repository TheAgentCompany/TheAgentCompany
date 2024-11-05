import json
from typing import List
import os
import time

from scoring import Result, Checkpoint
from common import create_rocketchat_client, num_rocketchat_users_contacted

CHECKPOINT_1_POINTS = 1
CHECKPOINT_2_POINTS = 5
CHECKPOINT_3_POINTS = 5

rocket = create_rocketchat_client()

ROCKETCHAT_URL = "http://the-agent-company.com:3000/home"

TEAM = ["mark_johnson", "sarah_johnson", "li_ming", "zhang_wei", "mike_chen"]
VALID_PASSWORDS = ["Fl0w3r#Br1ght", "Tr@ff1cL1ght99", "Dragon2024@Fly", "Cl0ud#Danc3r15", "Sunsh1ne@2024"]
VALID_PASSWORDS = dict(zip(TEAM, VALID_PASSWORDS))
NUM_USERS = len(TEAM)

def is_valid_password(user, password):
    return user in VALID_PASSWORDS and password == VALID_PASSWORDS[user]

def grade_checkpoint1(trajectory):
    return ROCKETCHAT_URL in trajectory

def grade_checkpoint2():
    return num_rocketchat_users_contacted(rocket, TEAM)

def grade_checkpoint3():
    num_valid_passwords = 0
    if not os.path.exists("/workspace/passwords.txt"):
        return 0
    with open("/workspace/passwords.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            items = line.strip().split(": ")
            if len(items) != 2:
                continue
            user, password = items[0], items[1]
            num_valid_passwords += is_valid_password(user, password)
    return min(num_valid_passwords, NUM_USERS)

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    points2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, points2))

    points3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(CHECKPOINT_3_POINTS, points3))
    return result