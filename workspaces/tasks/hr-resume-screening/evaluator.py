import logging

from common import create_rocketchat_client
from common import llm_evaluate
from common import get_chat_history

# Initialize RocketChat client
rocket = create_rocketchat_client()

def check_final_result(username: str):
    success, msg = get_chat_history(username)

    if not success:
        logging.warning(f"Failed to get history or no history")
        return False

    messages = [{"content": f"Does the message \"\"{msg}\"\" indicate Jane Lee cannot be hired because she fails to meet visa/green card/citizenship requirement? Please answer 'yes' if it does, or 'no' if it doesn't.", "role": "user"}]
    # Check result
    llm_resonse = llm_evaluate(messages)
    logging.info('LLM evaluator response is', llm_resonse)

    if 'yes' in llm_resonse['choices'][0]['message']['content'].lower():
        logging.info(f"{username} received expected conclusion")
        return True
    else:
        logging.info(f"{username} didn't receive expected conclusion")
        return False


def run_checkpoint_1():
    _, msgs = get_chat_history('Chen Xinyi')
    if msgs is not None and ('green card' in msgs.lower() or 'citizen' in msgs.lower()):
        return True
    return False


def run_checkpoint_2():
    return check_final_result('Li Ming')


if __name__ == "__main__":
    points = run_checkpoint_1() + 2 * run_checkpoint_2()
    print(f"Evaluation completed. Final score: {points}/3")
