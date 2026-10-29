"""Focused tests for the event-endpoint checkpoint's bounded request."""

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
            # Ensure this import resolves to the task's actual shared common.py,
            # regardless of what another test has loaded under the same name.
            sys.modules.pop("common", None)
            sys.modules.pop("config", None)
            importlib.import_module("common")

            spec = importlib.util.spec_from_file_location(
                "sde_debug_crashed_server_evaluator", TASK_DIR / "evaluator.py"
            )
            evaluator_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(evaluator_module)
            return evaluator_module
        finally:
            sys.path[:] = original_path


evaluator = load_evaluator()


class GradeCheckpoint5TimeoutTests(unittest.TestCase):
    def test_bounds_request_and_keeps_success_criteria(self):
        response = type("Response", (), {"text": "Enterprise-wide user-facing open architecture"})()
        with patch.object(evaluator.requests, "get", return_value=response) as get:
            self.assertTrue(evaluator.grade_checkpoint5())

        get.assert_called_once_with("http://localhost:5000/events", timeout=180)

    def test_timeout_is_a_failed_checkpoint(self):
        with patch.object(
            evaluator.requests,
            "get",
            side_effect=evaluator.requests.Timeout("slow endpoint"),
        ) as get:
            self.assertFalse(evaluator.grade_checkpoint5())

        get.assert_called_once_with("http://localhost:5000/events", timeout=180)


if __name__ == "__main__":
    unittest.main()
