import logging
from common import check_repo_exists
from scoring import Result, Checkpoint, bonus_for_completing_final

def grade_checkpoint1(trajectory):
    return (
        "/root/janusgraph" and "/root/janusgraph/-/blob/main/LICENSE?ref_type=heads"
        in trajectory
    )

def grade_checkpoint2():
    return check_repo_exists("janusgraph")

def grade_checkpoint3():
    try:
        if check_repo_exists("janusgraph"):
            with open("/workspace/janusgraph/LICENSE.txt") as f:
                code_content = f.read()
                if "APACHE-2.0" in code_content and "CC-BY-4.0" not in code_content:
                    return True
    except Exception as e:
        logging.warning(f"Error checking license: {e}")
    return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    return result
