import requests
import os
import logging
from typing import List
import json

from scoring import Result, Checkpoint
from config import *
from common import *

############################# init variable #####################################
PROJECT_NAME = "risingwave"
TARGET_FILE = "src/meta/src/controller/utils.rs"

############################# helper functions #####################################

def open_merge_request_exists(project_id, merge_request_title):
    merge_request = get_gitlab_merge_request_by_title(project_id, merge_request_title) if project_id else None
    return merge_request is not None and merge_request['state'] == 'opened'

def get_merge_request_file_changes(project_id, merge_request):
    merge_request_diffs = make_gitlab_request(project_id,f"merge_requests/{merge_request['iid']}/diffs") if merge_request is not None and 'iid' in merge_request else None
    if merge_request_diffs is None:
        merge_request_diffs = []
    else:
        merge_request_diffs = merge_request_diffs.json()

    file_changes = []

    for diff in merge_request_diffs:
        file_change =  diff
        file_change['added'] = []
        file_change['deleted'] = []

        for line in diff["diff"].splitlines():
            if line.startswith('@@'):
                continue
             # Added lines start with '+'
            if line.startswith('+'):
                content = line[1:]  # Remove the '+' prefix
                if content:  # Skip empty lines
                    file_change['added'].append(content)

            # Deleted lines start with '-'
            elif line.startswith('-'):
                content = line[1:]  # Remove the '-' prefix
                if content:  # Skip empty lines
                    file_change['deleted'].append(content)
        file_changes.append(file_change)
    return file_changes


############################# grade checkpoints #####################################

def grade_checkpoint1():
    return check_repo_exists(PROJECT_NAME)

def grade_checkpoint2():
    old_line = "pub vnode_count: i64,"
    file_path = os.path.join('/workspace', PROJECT_NAME, TARGET_FILE)
    if not os.path.exists(file_path):
        logging.warning(f"{file_path} does not exist")
        return False
    with open(file_path, 'r') as f:
        for line in f:
            line=line.strip()
            if line == old_line:
                logging.warning("The original target line was not deleted")
                return False
    return True

def grade_checkpoint3():
    new_line = "pub vnode_count: i32,"
    file_path = os.path.join('/workspace', PROJECT_NAME, TARGET_FILE)
    if not os.path.exists(file_path):
        logging.warning(f"{file_path} does not exist")
        return False
    with open(file_path, 'r') as f:
        for line in f:
            line=line.strip()
            if line == new_line:
                logging.warning("")
                return True
    logging.warning(f"Did not find the modified target line")
    return False


def grade_checkpoint4(project_id):
    return open_merge_request_exists(project_id, "fix(meta): fix vnode count data type when querying system table rw_fragments")

def grade_checkpoint5(project_id):
    merge_request = get_gitlab_merge_request_by_title(project_id,"fix(meta): fix vnode count data type when querying system table rw_fragments") if project_id else None
    file_changes = get_merge_request_file_changes(project_id, merge_request)
    if len(file_changes)!=1:
        logging.warning("Files changed not equal to 1.")
        return False
    if file_changes[0]['renamed_file'] or file_changes[0]['deleted_file'] or file_changes[0]['new_file']:
        logging.warning("File renamed, created or deleted.")
        return False
    if len(file_changes[0]['added'])!=1 or len(file_changes[0]['deleted'])!=1:
        logging.warning("Added or deleted lines not equal to 1.")
        return False
    if file_changes[0]['added'][0].strip() != "pub vnode_count: i32," or file_changes[0]['deleted'][0].strip() != "pub vnode_count: i64,":
        logging.warning("Added or deleted lines not correct.")
        return False
    return True



def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    project_id = get_gitlab_project_id(PROJECT_NAME)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4(project_id))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint5(project_id))))

    return result
