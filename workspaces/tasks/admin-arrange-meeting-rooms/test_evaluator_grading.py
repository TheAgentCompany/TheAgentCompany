"""Regression tests for the meeting-room answer message checkpoint."""

import importlib
import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


TASK_DIR = Path(__file__).resolve().parent
BASE_IMAGE_DIR = TASK_DIR.parents[1] / "base_image"


def load_evaluator():
    """Load the evaluator with the production grader and isolated optional deps."""
    litellm_stub = ModuleType("litellm")
    rocketchat_package_stub = ModuleType("rocketchat_API")
    rocketchat_package_stub.__path__ = []
    rocketchat_module_stub = ModuleType("rocketchat_API.rocketchat")

    class DummyRocketChat:
        def __init__(self, *args, **kwargs):
            pass

    rocketchat_module_stub.RocketChat = DummyRocketChat

    dependencies = {
        "litellm": litellm_stub,
        "rocketchat_API": rocketchat_package_stub,
        "rocketchat_API.rocketchat": rocketchat_module_stub,
    }
    with patch.dict(sys.modules, dependencies):
        original_path = sys.path[:]
        sys.path.insert(0, str(BASE_IMAGE_DIR))
        try:
            sys.modules.pop("common", None)
            sys.modules.pop("config", None)
            importlib.import_module("common")

            spec = importlib.util.spec_from_file_location(
                "admin_arrange_meeting_rooms_evaluator", TASK_DIR / "evaluator.py"
            )
            evaluator_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(evaluator_module)
            return evaluator_module
        finally:
            sys.path[:] = original_path


evaluator = load_evaluator()


class MeetingRoomMessageGradingTests(unittest.TestCase):
    def evaluate_message(self, message, sender="theagentcompany"):
        with patch.object(
            evaluator,
            "get_rocketchat_personal_chat_history",
            return_value=[{"msg": message, "u": {"username": sender}}],
        ) as history:
            result = evaluator.grade_checkpoint_2()

        history.assert_called_once_with(evaluator.rocket_client, "Chen Xinyi", content_only=False)
        return result

    def test_correct_room_count_is_accepted_with_other_numbers(self):
        answer = evaluator.REFERENCE_ANSWER
        self.assertTrue(
            self.evaluate_message(
                f"We need {answer} rooms for the {answer + 1} teams; minimum is {answer}."
            )
        )

    def test_times_decimals_prices_and_wrong_counts_do_not_match(self):
        answer = evaluator.REFERENCE_ANSWER
        wrong_answer = answer + 1
        messages = [
            f"Let's meet at {answer}:30pm to discuss room booking.",
            f"I will call you at 1{answer}:00.",
            f"The estimate is {answer}.5 rooms.",
            f"The total is ${answer}5.",
            f"We need {wrong_answer} rooms; let's discuss at {answer}:30pm.",
        ]

        for message in messages:
            with self.subTest(message=message):
                self.assertFalse(self.evaluate_message(message))

    def test_recipient_reply_does_not_count_as_agent_answer(self):
        answer = evaluator.REFERENCE_ANSWER
        self.assertFalse(self.evaluate_message(f"We need {answer} rooms.", sender="chenxinyi"))


if __name__ == "__main__":
    unittest.main()
