"""Focused integration checks for authenticated GitLab readiness."""

import importlib.util
import io
import pathlib
import sys
import threading
import types
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch


API_DIR = pathlib.Path(__file__).resolve().parents[1]


def load_api_server():
    rocketchat_package = types.ModuleType("rocketchat_API")
    rocketchat_module = types.ModuleType("rocketchat_API.rocketchat")
    rocketchat_module.RocketChat = object
    redis_module = types.ModuleType("redis")
    redis_module.StrictRedis = object
    redis_exceptions = types.ModuleType("redis.exceptions")
    redis_exceptions.ConnectionError = ConnectionError
    redis_module.exceptions = redis_exceptions
    redis_om = types.ModuleType("redis_om")
    redis_om.JsonModel = object
    redis_om_model = types.ModuleType("redis_om.model")
    redis_om_model_model = types.ModuleType("redis_om.model.model")
    redis_om_model_model.Field = lambda **kwargs: None

    dependencies = {
        "rocketchat_API": rocketchat_package,
        "rocketchat_API.rocketchat": rocketchat_module,
        "redis": redis_module,
        "redis.exceptions": redis_exceptions,
        "redis_om": redis_om,
        "redis_om.model": redis_om_model,
        "redis_om.model.model": redis_om_model_model,
    }
    utils_spec = importlib.util.spec_from_file_location(
        "gitlab_health_test_utils", API_DIR / "utils.py"
    )
    utils = importlib.util.module_from_spec(utils_spec)
    real_open = open

    def open_runtime_file(path, *args, **kwargs):
        if path == "/rocketchat/npc_definition.json":
            return io.StringIO("[]")
        return real_open(path, *args, **kwargs)

    with patch.dict(sys.modules, dependencies), patch("builtins.open", open_runtime_file):
        utils_spec.loader.exec_module(utils)

    api_spec = importlib.util.spec_from_file_location(
        "gitlab_health_test_api", API_DIR / "api-server.py"
    )
    api_server = importlib.util.module_from_spec(api_spec)
    with patch.dict(sys.modules, {"utils": utils}):
        api_spec.loader.exec_module(api_server)
    return api_server, utils


class GitLabHealthcheckTests(unittest.TestCase):
    def test_route_requires_authenticated_projects_api_to_be_healthy(self):
        class GitLabHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != "/api/v4/projects":
                    status = 404
                elif self.headers.get("PRIVATE-TOKEN") == "root-token":
                    status = 200
                else:
                    status = 401
                self.send_response(status)
                self.send_header("Content-Length", "0")
                self.end_headers()

            def log_message(self, format, *args):
                pass

        api_server, _ = load_api_server()
        server = ThreadingHTTPServer(("127.0.0.1", 0), GitLabHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server_thread.join, 2)
        self.addCleanup(server.shutdown)

        with patch.object(
            api_server,
            "GITLAB_HEALTH_URL",
            f"http://127.0.0.1:{server.server_port}/api/v4/projects",
        ):
            healthy = api_server.app.test_client().get("/api/healthcheck/gitlab")
            self.assertEqual(healthy.status_code, 200)

            with patch.object(api_server, "GITLAB_HEALTH_HEADERS", {}):
                unauthorized = api_server.app.test_client().get("/api/healthcheck/gitlab")
            self.assertEqual(unauthorized.status_code, 401)

    def test_health_request_has_finite_connect_and_read_timeouts(self):
        _, utils = load_api_server()
        response = types.SimpleNamespace(status_code=200)
        headers = {"PRIVATE-TOKEN": "root-token"}
        with patch.object(utils.requests, "get", return_value=response) as get:
            status, _ = utils.check_url("http://gitlab.example/api/v4/projects", headers=headers)

        self.assertEqual(status, 200)
        get.assert_called_once_with(
            "http://gitlab.example/api/v4/projects", headers=headers, timeout=(5, 15)
        )


if __name__ == "__main__":
    unittest.main()
