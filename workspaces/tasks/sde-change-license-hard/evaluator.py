import logging
from common import check_repo_exists
from scoring import Result, Checkpoint, bonus_for_completing_final

def grade_checkpoint1(trajectory):
    return (
        "/root/janusgraph" and "/root/colly" and "/root/streamlit"
        in trajectory
    )

def grade_checkpoint2():
    return check_repo_exists("janusgraph") and check_repo_exists("colly") and check_repo_exists("streamlit")

def grade_checkpoint3():
    try:
        with open("/workspace/janusgraph/LICENSE.txt") as f:
            code_content = f.read()
            if "APACHE-2.0" not in code_content and "CC-BY-4.0" not in code_content and "MIT" in code_content:
                return True
        with open("/workspace/colly/LICENSE.txt") as f:
            code_content = f.read()
            if "Apache License" not in code_content and "MIT" in code_content:
                return True
        with open("/workspace/streamlit/LICENSE") as f:
            code_content = f.read()
            if "Apache License" not in code_content and "MIT" in code_content:
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

    passed3 = passed2 and grade_checkpoint3()
    checkpoints.append(Checkpoint(1, int(passed3)))

    return result