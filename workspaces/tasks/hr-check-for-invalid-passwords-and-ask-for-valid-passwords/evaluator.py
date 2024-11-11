from typing import List
import os

from scoring import Result, Checkpoint
from common import create_rocketchat_client, num_rocketchat_users_contacted, checkpoint

CHECKPOINT_1_POINTS = 2
CHECKPOINT_2_POINTS = 2

rocket = create_rocketchat_client()

USERS_WITH_INVALID_PASSWORDS = ["mark_johnson", "mike_chen"]
USERS_WITH_VALID_PASSWORDS = ["sarah_johnson", "li_ming", "zhang_wei"]
VALID_PASSWORDS = {
    "mark_johnson": "Fl0w3r#Br1ght",
    "sarah_johnson": "Tr@ff1cL1ght99",
    "li_ming": "Dragon2024@Fly",
    "zhang_wei": "Cl0ud#Danc3r15",
    "mike_chen": "Sunsh1ne@2024"
}
NUM_USERS = 5

def is_valid_password(user, password):
    return user in VALID_PASSWORDS and password == VALID_PASSWORDS[user]

@checkpoint
def grade_checkpoint1():
    return num_rocketchat_users_contacted(rocket, USERS_WITH_INVALID_PASSWORDS) == len(USERS_WITH_INVALID_PASSWORDS) and num_rocketchat_users_contacted(rocket, USERS_WITH_VALID_PASSWORDS) == 0

@checkpoint
def grade_checkpoint2():
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
    return num_valid_passwords == NUM_USERS

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(CHECKPOINT_1_POINTS, CHECKPOINT_1_POINTS * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(CHECKPOINT_2_POINTS, CHECKPOINT_2_POINTS * int(passed2)))
    return result