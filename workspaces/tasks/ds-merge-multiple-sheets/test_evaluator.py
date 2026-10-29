"""Regression tests for malformed and unmatched merged-sheet rows."""

import importlib
import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pandas as pd


TASK_DIR = Path(__file__).resolve().parent
BASE_IMAGE_DIR = TASK_DIR.parents[1] / "base_image"


def load_evaluator():
    """Load production evaluator/common code with only unavailable deps stubbed."""
    litellm_stub = ModuleType("litellm")
    requests_stub = ModuleType("requests")
    requests_stub.__path__ = []
    requests_auth_stub = ModuleType("requests.auth")
    requests_auth_stub.HTTPBasicAuth = object
    rocketchat_package_stub = ModuleType("rocketchat_API")
    rocketchat_package_stub.__path__ = []
    rocketchat_module_stub = ModuleType("rocketchat_API.rocketchat")

    class DummyRocketChat:
        def __init__(self, *args, **kwargs):
            pass

    rocketchat_module_stub.RocketChat = DummyRocketChat
    dependencies = {
        "litellm": litellm_stub,
        "requests": requests_stub,
        "requests.auth": requests_auth_stub,
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
                "ds_merge_multiple_sheets_evaluator", TASK_DIR / "evaluator.py"
            )
            evaluator_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(evaluator_module)
            return evaluator_module
        finally:
            sys.path[:] = original_path


evaluator = load_evaluator()


class FoundMatchingRowTests(unittest.TestCase):
    def setUp(self):
        self.expected = [[1, ["sugar source"], 10.0]]

    def test_correct_row_matches(self):
        data = pd.DataFrame([[1, "Sugar source A", 10.0]])

        self.assertTrue(evaluator.found_matching_row(data, self.expected))

    def test_wrong_row_does_not_match(self):
        data = pd.DataFrame([[2, "Sugar source A", 10.0]])

        self.assertFalse(evaluator.found_matching_row(data, self.expected))

    def test_missing_expected_row_does_not_match(self):
        expected = [
            [1, ["sugar source"], 10.0],
            [2, ["fruit juice"], 8.0],
        ]
        data = pd.DataFrame([[1, "Sugar source A", 10.0]])

        self.assertFalse(evaluator.found_matching_row(data, expected))

    def test_non_string_keyword_column_does_not_pass_after_str_error(self):
        data = pd.DataFrame([[1, 17.2, 10.0]])

        self.assertFalse(evaluator.found_matching_row(data, self.expected))


if __name__ == "__main__":
    unittest.main()
