from common import create_rocketchat_client
from llm_evaluator import *

# Initialize RocketChat client
rocket = create_rocketchat_client()

############################# Helper Functions #####################################

def get_history(username: str):
    id = ""
    for item in rocket.users_list().json()['users']:
        if item['nameInsensitive'] == username.lower():
            id = item["_id"]
            break
    msgs = rocket.im_history(room_id=id).json()['messages']
    for msg in msgs[::-1]:
        print(f"{username}'s chat: {msg['msg']}")

    if len(msgs)>0:
        return True, msg
    else:
        return False, None


def check_final_feedback(username: str):

    success, msg = get_history(username)

    if not success:
        print(f"Failed to get history or no history")
        return False

    messages = [{"content": f"Does the phrase \"\"{msg}\"\" indicate the person receiving the feedback had an average job performance? Please answer 'yes' if it does, or 'no' if it doesn't.", "role": "user"}]
    # Check result
    llm_resonse = llm_evaluator(messages).json()
    print(llm_resonse)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        print(f"{username} received feedback that indicates an average job performance")
        return True
    else:
        print(f"{username} did not receive feedback that indicates an average job performance")
        return False

############################# Evaluator #####################################

def evaluate_task():
    points = 0

    npcs = ["Mike Chen", "Li Ming", "Zhang Wei"]
    performance_evaluatee = "Liu Qiang"

    for npc in npcs:
        res, _ = get_history(npc)
        if res:
            points += 1

    if check_final_feedback(performance_evaluatee):
        points += 2

    # Final result
    print(f"Evaluation completed. Final score: {points}/5")
    return points

if __name__ == "__main__":
    evaluate_task()
