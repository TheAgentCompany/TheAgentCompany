import requests
import logging
import os
import sys
from rocketchat_API.rocketchat import RocketChat  # type: ignore

SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME") or "the-agent-company.com"
ROCKETCHAT_PORT = os.getenv("ROCKETCHAT_PORT") or "3000"
channel_name = "general"
ROCKETCHAT_URL = f"http://{SERVER_HOSTNAME}:{ROCKETCHAT_PORT}"

from common import create_rocketchat_client, evaluate_with_llm

user_room_mapping = {
    "Mark Johnson": "CZYWHd5bCmhj5YcFeRGZyENbrjkxjosMCH",
    "Jessica Lee": "4qnpxztMbfyYn3rQACZYWHd5bCmhj5YcFe",
    "David Wong": "CZYWHd5bCmhj5YcFeGTcEyGXzbKiLmQxFc",
    "Emily Zhou": "CZYWHd5bCmhj5YcFeppuM42XhPD79wwxMv",
    "Chen Xinyi": "CZYWHd5bCmhj5YcFec2uqaen3naCexvzDE",
}
TARGET_STRING = "We identified a promising candidate whose tech stack matches your expertise. Would you be available to conduct a technical interview this week?"
LEADER_NAME = "Chen Xinyi"
TARGET_INTERVIEWER = "Emily Zhou"

# Create RocketChat instance
rocket = create_rocketchat_client()


def grade_checkpoint1():
    # [2pts] Check the chat history with the leader Chen Xinyi
    try:
        messages = get_direct_messages(user_room_mapping[LEADER_NAME])
        composed_messages = compose_messages(messages)
        chat_with_leader = evaluate_with_llm(
            content=composed_messages,
            predicate=f"the examinee has a chat with the leader {LEADER_NAME} on the interviewer (there could be some irrelevant messages, but if could can find any message that is related to the interviewer, it should be considered as a chat)",
            additional_prompt="",
        )

        if not chat_with_leader:
            logging.error(f"There is no direct message with leader {LEADER_NAME}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error fetching message data or evaluating: {e}")
        return False


def grade_checkpoint2():
    # [2pts] Check whether examinee chat with Emily Zhou (the right person).
    try:
        messages = get_direct_messages(user_room_mapping[TARGET_INTERVIEWER])
        composed_messages = compose_messages(messages)
        chat_with_interviewer = evaluate_with_llm(
            content=composed_messages,
            predicate=f"there is a chat on inquiring whether the someone is available for a technical interview",
            additional_prompt="",
        )

        if not chat_with_interviewer:
            logging.error(
                f"The hr does not send the right message to the potential interviewer {TARGET_INTERVIEWER}"
            )
            return False

    except Exception as e:
        logging.error(f"Error fetching message data: {e}")
        return False

    return True


def grade_checkpoint3():
    # [2pts] Check whether examinee does not chat with others (Mike Chen, Wang Fang, David Wong, Huang Jie)

    target_names = ["Mark Johnson", "Jessica Lee", "David Wong"]
    for name in target_names:
        try:
            messages = get_direct_messages(user_room_mapping[name])
            composed_messages = compose_messages(messages)
            chat_with_other = evaluate_with_llm(
                content=composed_messages,
                predicate=f"there is a chat on inquiring whether the someone is available for a technical interview",
                additional_prompt="",
            )

            if chat_with_other:
                logging.error(
                    f"The examinee sent the message to {name} who is not a match"
                )
                return False

        except Exception as e:
            logging.error(f"Error fetching message data: {e}")
            return False

    return True


def get_direct_messages(room_id):
    response = rocket.im_history(room_id=room_id).json()
    if not response.get("success"):
        print(f"Failed to retrieve DM history. Room ID: {room_id}")
        return None

    messages = response.get("messages", [])
    return messages


def compose_messages(messages):
    return "\n".join(
        f"Message {i+1}: {msg.get('msg', '')}" for i, msg in enumerate(messages)
    )


if __name__ == "__main__":
    passed1 = grade_checkpoint1()
    passed2 = grade_checkpoint2()
    passed3 = grade_checkpoint3()
    print(f"Checkpoint 1: {'✓' if passed1 else '✗'}")
    print(f"Checkpoint 2: {'✓' if passed2 else '✗'}")
    print(f"Checkpoint 3: {'✓' if passed3 else '✗'}")
    points = 2 * int(passed1) + 2 * int(passed2) + 2 * int(passed3)
    print(f"Final points: {points}")
