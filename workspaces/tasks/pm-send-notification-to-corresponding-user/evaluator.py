from common import evaluate_with_llm
from common import create_rocketchat_client

# Create RocketChat instance
rocket = create_rocketchat_client()


def get_history(username):
    id = ""
    for item in rocket.users_list().json()['users']:
        if item['username'] == username:
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']
    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")

    return msgs

def check_with_llm(msgs):
    content = ""
    for msg in msgs[::-1]:
        content += msg['msg']

    if len(content)==0:
        return False

    predicate = 'there is a plan to hold a kickoff meeting for the main Q4 project'
    return evaluate_with_llm(content, predicate)


def checkpoint1(username='jessica_lee'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

def checkpoint2(username='david_wong'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

def checkpoint3(username='huang_jie'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)

def checkpoint4(username='mark_johnson'):
    msgs = get_history(username=username)
    return check_with_llm(msgs)


def calculate_total_score():
    # Define the scores corresponding to when each function is True
    scores = {
        checkpoint1: 1,
        checkpoint2: 1,
        checkpoint3: 1,
        checkpoint4: 1,

    }

    total_score = 0

    for func, score in scores.items():
        if func():
            total_score += score

    return total_score

# compute the total point
total = calculate_total_score()
print(f"\ntotal point is: {total}")

