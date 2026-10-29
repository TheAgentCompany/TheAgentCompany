"""Focused tests for the event-endpoint checkpoint's bounded request."""

import importlib.util
import functools
import sys
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


TASK_DIR = Path(__file__).resolve().parent
BASE_IMAGE_DIR = TASK_DIR.parents[1] / "base_image"
sys.path.insert(0, str(BASE_IMAGE_DIR))


def grader(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return False

    return wrapper


common_stub = ModuleType("common")
common_stub.create_rocketchat_client = lambda: object()
common_stub.get_rocketchat_personal_chat_history = lambda *args, **kwargs: []
common_stub.grader = grader
sys.modules["common"] = common_stub

spec = importlib.util.spec_from_file_location("sde_debug_crashed_server_evaluator", TASK_DIR / "evaluator.py")
evaluator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluator)


class GradeCheckpoint5TimeoutTests(unittest.TestCase):
    def test_bounds_request_and_keeps_success_criteria(self):
        response = type("Response", (), {"text": "Enterprise-wide user-facing open architecture"})()
        with patch.object(evaluator.requests, "get", return_value=response) as get:
            self.assertTrue(evaluator.grade_checkpoint5())

        get.assert_called_once_with("http://localhost:5000/events", timeout=180)

    def test_timeout_is_a_failed_checkpoint(self):
        with patch.object(evaluator.requests, "get", side_effect=evaluator.requests.Timeout("slow endpoint")) as get:
            self.assertFalse(evaluator.grade_checkpoint5())

        get.assert_called_once_with("http://localhost:5000/events", timeout=180)

if __name__ == "__main__":
    unittest.main()
