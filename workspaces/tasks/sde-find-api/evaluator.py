import logging
import json
from typing import List
from scoring import Result, Checkpoint

from common import evaluate_with_llm, grader


@grader
def grade_checkpoint1():
    # [2pts] Read `/workspace/url_for_issues.txt`, check if the agent find the correct url `http://the-agent-company:8091/api/workspaces/{workspace_name}/issues/` (in our case `workspace_name` is `tac`)
    try:
        with open("/workspace/url_for_issues.txt", "r") as f:
            url = f.read()
            if not evaluate_with_llm(
                content=url,
                predicate="the agent provides a url and the url has the same pattern as `http://the-agent-company.com:8091/api/workspaces/tac/issues/`",
            ):
                logging.error(
                    f"The correct url does not exist in the `/workspace/url_for_issues.txt`"
                )
                return False
            return True
    except Exception as e:
        logging.error(f"Error reading solution file: {e}")
        return False


@grader
def grade_checkpoint2():
    # [2pts] Check whether examinee get the correct parameter `order_by=-target_date, per_page=10, cursor=10:0:0`

    try:
        with open("/workspace/url_for_issues.txt", "r") as f:
            parameters = f.read()
            if not evaluate_with_llm(
                content=parameters,
                predicate="the agent provides the correct parameters `order_by=-target_date, per_page=10, cursor=10:0:0` (the order of the parameters and the way they are provided does not matter)",
            ):
                logging.error(
                    f"The correct parameters does not exist in the `/workspace/parameters.txt`"
                )
                return False
            return True
    except Exception as e:
        logging.error(f"Error reading solution file: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    passed1 = grade_checkpoint1()
    passed2 = grade_checkpoint2()

    checkpoints.append(Checkpoint(2, 2 * int(passed1)))
    checkpoints.append(Checkpoint(2, 2 * int(passed2)))

    return result
