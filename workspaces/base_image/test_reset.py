"""Regression coverage for HTTP failures in the production reset script."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


RESET_SCRIPT = Path(__file__).resolve().with_name("reset.sh")


class ResetScriptHttpTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        self.curl_log = self.root / "curl.log"
        self.sleep_log = self.root / "sleep.log"

        self._write_executable(
            "grep",
            """#!/bin/sh
case "$*" in
    *rocketchat*) exit 0 ;;
    *) exit 1 ;;
esac
""",
        )
        self._write_executable(
            "curl",
            """#!/bin/sh
printf '%s\\n' "$*" >> "$CURL_LOG"
case "$*" in
    *"-X POST"*)
        if [ "$HTTP_ERROR" = "1" ]; then
            case "$*" in
                *--fail-with-body*) printf 'reset rejected\\n'; exit 22 ;;
                *) printf 'reset rejected\\n'; exit 0 ;;
            esac
        fi
        printf 'reset accepted\\n'
        ;;
    *) printf '200' ;;
esac
""",
        )
        self._write_executable(
            "sleep",
            """#!/bin/sh
printf '%s\\n' "$*" >> "$SLEEP_LOG"
exit 99
""",
        )

    def _write_executable(self, name, contents):
        path = self.bin_dir / name
        path.write_text(contents)
        path.chmod(0o755)

    def _run_reset(self, http_error):
        env = os.environ.copy()
        env.update(
            {
                "PATH": f"{self.bin_dir}{os.pathsep}{env['PATH']}",
                "CURL_LOG": str(self.curl_log),
                "SLEEP_LOG": str(self.sleep_log),
                "HTTP_ERROR": "1" if http_error else "0",
            }
        )
        return subprocess.run(
            ["bash", str(RESET_SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def test_http_error_from_reset_is_not_accepted_as_healthy_old_service(self):
        result = self._run_reset(http_error=True)

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        requests = self.curl_log.read_text().splitlines()
        self.assertEqual(len(requests), 1, requests)
        self.assertIn("--fail-with-body", requests[0])
        self.assertIn("--connect-timeout 10", requests[0])
        self.assertIn("--max-time 1800", requests[0])
        self.assertFalse(self.sleep_log.exists(), "must stop before polling old service health")

    def test_successful_reset_waits_until_healthcheck_returns_200_without_sleeping(self):
        result = self._run_reset(http_error=False)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        requests = self.curl_log.read_text().splitlines()
        self.assertEqual(len(requests), 2, requests)
        self.assertIn("--connect-timeout 10", requests[0])
        self.assertIn("--max-time 1800", requests[0])
        self.assertIn("-I", requests[1])
        self.assertIn("--connect-timeout 5", requests[1])
        self.assertIn("--max-time 15", requests[1])
        self.assertFalse(self.sleep_log.exists(), "healthy services should not incur a polling delay")


if __name__ == "__main__":
    unittest.main()
