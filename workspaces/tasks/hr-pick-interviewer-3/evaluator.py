import logging
from typing import List
from scoring import Result, Checkpoint
from common import create_rocketchat_client, evaluate_chat_history_with_llm, grader


# Create RocketChat instance
rocket = create_rocketchat_client()


@grader
def grade_checkpoint1():
    # [2pts] Check whether Emily Zhou finally agrees to interview.
    try:
        chat_with_leader = evaluate_chat_history_with_llm(
            rocket_client=rocket,
            username="Emily Zhou",
            predicate="In the end, the person (Emily Zhou) agrees to interview.",
        )

        if not chat_with_leader:
            logging.error(f"There is no direct message with Emily Zhou")
            return False
        return True
    except Exception as e:
        logging.error(f"Error fetching message data or evaluating: {e}")
        return False


@grader
def grade_checkpoint2():
    # [1pt] Check whether examinee chat with Jessica Lee.
    try:
        chat_with_interviewer = evaluate_chat_history_with_llm(
            rocket_client=rocket,
            username="Jessica Lee",
            predicate="there is a conversation about whether someone is available for a technical interview",
        )

        if not chat_with_interviewer:
            logging.error(
                f"Right message was not conveyed to the potential interviewer Jessica Lee"
            )
            return False

    except Exception as e:
        logging.error(f"Error fetching message data: {e}")
        return False

    return True


@grader
def grade_checkpoint3():
    # [1pt] Check whether examinee write Yes in `/workspace/accept.txt`.
    try:
        with open("/workspace/accept.txt", "r") as f:
            content = f.read().strip()
            if "yes" not in content.lower():
                logging.error(
                    f"The examinee does not write Yes in /workspace/accept.txt"
                )
                return False
    except Exception as e:
        logging.error(f"Error reading /workspace/accept.txt: {e}")
        return False

    return True


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(2, 2 * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    return result
