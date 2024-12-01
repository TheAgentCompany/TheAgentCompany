import csv

from typing import List

from litellm import logging

from scoring import Result, Checkpoint
from common import *

rocket = create_rocketchat_client()

@grader
def checkpoint1():
    logging.warning('Emma Lewis was not contacted.')
    return bool(get_rocketchat_personal_chat_history(rocket, 'Emma Lewis'))

@grader
def checkpoint2():
    logging.warning('Sarah Johnson was not contacted.')
    return bool(get_rocketchat_personal_chat_history(rocket, 'Sarah Johnson'))

@grader
def checkpoint3():
    filenames=[
        'cloudtech_industries_quote.pdf',
        'datacore_enterprise_quote.pdf',
        'netsys_corporation_quote.pdf',
        'servermaster_systems_quote.pdf',
        'techpro_solutions_quote.pdf'
    ]
    for filename in filenames:
        if not os.path.exists(os.path.join('/workspace',filename)):
            logging.warning(f'{filename} not downloaded')
            return False
    return True

@grader
def checkpoint4():
    file_check = check_file_in_owncloud_directory('valid-quotes.csv','Documents/Administrative%20Specialist')
    if file_check is None:
        return False
    return file_check

@grader
def checkpoint5():
    sarah_chat = get_rocketchat_personal_chat_history(rocket, 'Sarah Johnson')
    if len(sarah_chat) == 0:
        logging.warning('No chat found with Sarah Johnson')
        return False
    #Extracting link from the last chat
    link = re.search(r'(https?://ogma.lti.cs.cmu.edu/s/[a-zA-Z0-9]+)', "\n".join(sarah_chat))
    if not link:
        logging.warning("Valid quotes link not found in Sarah Johnson's chat")
        return False
    return True

@grader
def checkpoint6():
    sarah_chat = get_rocketchat_personal_chat_history(rocket, 'Sarah Johnson')
    if len(sarah_chat) == 0:
        logging.warning('No chat found with Sarah Johnson')
        return False
    link = re.search(r'(https?://ogma.lti.cs.cmu.edu/s/[a-zA-Z0-9]+)', "\n".join(sarah_chat))
    if not link:
        logging.warning("Valid quotes link not found in Sarah Johnson's chat")
        return False
    else:
        download_owncloud_content(link.group(0) ,'/workspace/valid-quotes-downloaded.csv')
        with open('/workspace/valid-quotes-downloaded.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)
        if len(data[0].keys()) != 2:
            logging.warning('Invalid number of columns in downloaded csv')
            return False
        for key in data[0]:
            if key.strip().lower() not in ['name', 'price']:
                logging.warning('Invalid column name in downloaded csv')
                return False
        if len(data) != 2:
            logging.warning('Invalid number of rows in downloaded csv')
            return False
        if data[0]['name'].strip().lower() != 'netsys corporation' or data[0]['price'].strip() != '12199.99':
            logging.warning('Invalid data in downloaded csv')
            return False
        if data[1]['name'].strip().lower() != 'datacore enterprise' or data[1]['price'].strip() != '11999.99':
            logging.warning('Invalid data in downloaded csv')
            return False
    return True

def grade_checkpoints(trajectory=''):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, int(checkpoint1())))
    checkpoints.append(Checkpoint(1, int(checkpoint2())))
    checkpoints.append(Checkpoint(1, int(checkpoint3())))
    checkpoints.append(Checkpoint(1, int(checkpoint4())))
    checkpoints.append(Checkpoint(1, int(checkpoint5())))
    checkpoints.append(Checkpoint(1, int(checkpoint6())))
    return result

