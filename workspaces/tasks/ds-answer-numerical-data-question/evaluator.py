import logging
import os

from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm, grader


def read_from_docx(fn):
    # use python-docx to read the content of the docx file
    import docx

    doc = docx.Document(fn)
    return "\n".join([p.text for p in doc.paragraphs])


@grader
def grade_checkpoint1():
    # [2pts] The agent correctly answers the question 1 (Tea (including ice tea)).
    try:
        content = read_from_docx("/workspace/answer.docx")
        content = content.strip().split("\n")[0]
        if evaluate_with_llm(
            content=content,
            predicate="the content contains the correct answer `Tea (including ice tea)`",
        ):
            logging.info("Correct answer found in answer.docx for question 1.")
            return True
        else:
            logging.warning("Incorrect answer found in answer.docx.")
            return False

    except Exception as e:
        logging.error(f"Error in answer.docx: {e}")
        return False


@grader
def grade_checkpoint2():
    # [2pts] The agent correctly answers the question 2 (88.475)
    try:
        content = read_from_docx("/workspace/answer.docx")
        content = content.strip().split("\n")[1]
        if evaluate_with_llm(
            content=content,
            predicate="the content contains the correct answer `88.475`",
        ):
            logging.info("Correct answer found in answer.docx for question 2.")
            return True
        else:
            logging.warning("Incorrect answer found in answer.docx.")
            return False

    except Exception as e:
        logging.error(f"Error in answer.docx: {e}")
        return False


@grader
def grade_checkpoint3():
    # [2pts] The agent correctly answers the question 3 (74.775)

    try:
        content = read_from_docx("/workspace/answer.docx")
        content = content.strip().split("\n")[2]
        if evaluate_with_llm(
            content=content,
            predicate="the content has the correct answer `74.775`",
        ):
            logging.info("Correct answer found in answer.docx for question 3.")
            return True
        logging.warning("Incorrect answer found in answer.docx.")
        return False
    except Exception as e:
        logging.error(f"Error in answer.docx: {e}")
        return False


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    grading_functions = [
        (
            grade_checkpoint1,
            "The agent correctly answers the question 1 (Tea (including ice tea))",
        ),
        (grade_checkpoint2, "The agent correctly answers the question 2 (88.475)"),
        (grade_checkpoint3, "The agent correctly answers the question 3 (74.775)"),
    ]

    for grade_func, description in grading_functions:
        try:
            if callable(grade_func) and grade_func.__name__ == "<lambda>":
                passed = grade_func(trajectory)
            else:
                passed = grade_func()
            logging.info(f"{'✓' if passed else '✗'} {description}")
            checkpoints.append(Checkpoint(2, int(passed) * 2))
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")

    return result
