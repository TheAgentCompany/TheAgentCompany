import importlib.util
import io
import pathlib
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


UTILS_PATH = pathlib.Path(__file__).resolve().parents[1] / "utils.py"


def load_utils_module():
    rocketchat_package = types.ModuleType("rocketchat_API")
    rocketchat_module = types.ModuleType("rocketchat_API.rocketchat")
    rocketchat_module.RocketChat = object
    redis_om = types.ModuleType("redis_om")
    redis_om.JsonModel = object
    redis_om_model = types.ModuleType("redis_om.model")
    redis_om_model_model = types.ModuleType("redis_om.model.model")
    redis_om_model_model.Field = lambda **kwargs: None

    modules = {
        "rocketchat_API": rocketchat_package,
        "rocketchat_API.rocketchat": rocketchat_module,
        "redis_om": redis_om,
        "redis_om.model": redis_om_model,
        "redis_om.model.model": redis_om_model_model,
    }
    module_spec = importlib.util.spec_from_file_location("controller_utils_under_test", UTILS_PATH)
    module = importlib.util.module_from_spec(module_spec)
    real_open = open

    def open_runtime_file(path, *args, **kwargs):
        if path == "/rocketchat/npc_definition.json":
            return io.StringIO("[]")
        return real_open(path, *args, **kwargs)

    with patch.dict(sys.modules, modules), patch("builtins.open", open_runtime_file):
        module_spec.loader.exec_module(module)
    return module


def load_api_server_module(utils_module):
    module_spec = importlib.util.spec_from_file_location(
        "api_server_under_test", UTILS_PATH.parent / "api-server.py"
    )
    module = importlib.util.module_from_spec(module_spec)
    with patch.dict(sys.modules, {"utils": utils_module}):
        module_spec.loader.exec_module(module)
    return module


class ExecuteCommandTests(unittest.TestCase):
    def test_nonzero_exit_raises_instead_of_returning_success_like_text(self):
        utils = load_utils_module()

        with tempfile.TemporaryDirectory() as execution_dir:
            utils.EXECUTION_DIR = execution_dir
            with self.assertRaises(subprocess.CalledProcessError) as raised:
                utils.execute_command("exit 7")

        self.assertEqual(raised.exception.returncode, 7)

    def test_failed_synchronous_reset_returns_server_error(self):
        utils = load_utils_module()
        api_server = load_api_server_module(utils)
        failure = subprocess.CalledProcessError(1, "make reset-gitlab")

        with patch.object(api_server, "execute_command", side_effect=failure):
            response = api_server.app.test_client().post("/api/reset-gitlab")

        self.assertEqual(response.status_code, 500)
        self.assertNotIn(b"make reset-gitlab", response.data)

    def test_async_failure_is_logged_once_with_exception_details(self):
        utils = load_utils_module()
        failure = RuntimeError("background reset failed")

        with patch.object(utils, "execute_command", side_effect=failure):
            with self.assertLogs(level="ERROR") as captured:
                thread = utils.async_execute_command("make reset-plane")
                thread.join(timeout=5)

        self.assertFalse(thread.is_alive())
        self.assertEqual(len(captured.records), 1)
        self.assertIn("RuntimeError: background reset failed", captured.output[0])


if __name__ == "__main__":
    unittest.main()
