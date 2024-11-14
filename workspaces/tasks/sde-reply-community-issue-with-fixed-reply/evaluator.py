import sys
import logging

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm
from common import make_gitlab_request, grader

# Configuration for gitlab
project_path = "root/openhands"
issue_id = 4158


def get_gitlab_issue_notes():
    try:
        response = make_gitlab_request(project_path, f"issues/{issue_id}/notes")
        return response.json()
    except Exception as e:
        logging.error(f"Error occurred while checking the repository: {e}")
        return []

@grader
def grade_checkpoint1(trajectory: str):
    return 'root/openhands/-/issues/4158' in trajectory


@grader
def grade_checkpoint2():
    issue_notes = get_gitlab_issue_notes()
    if issue_notes:
        return any(issue_note.get('id') not in [127283, 127284, 127285] for issue_note in issue_notes)
    else:
        return False


@grader
def grade_checkpoint3():
    issue_notes = get_gitlab_issue_notes()
    target = None
    if issue_notes:
        for issue_note in issue_notes:
            if issue_note.get('id') not in [127283, 127284, 127285]:
                target = issue_note.get('body')
    else:
        return False

    if target is None:
        return False

    return evaluate_with_llm(
        'Alright, let\'s go ahead and increase the timeout limit bya few seconds on issue #4158 and monitory the result. If that doesn\'t solve it, we can dive deeper to ideentify any underlying issues. I\'ll start working on the update now.',
        predicate=target,
    )


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))

    return result


