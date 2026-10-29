import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("download.sh")
NAMES = ("docker-compose.yaml", "plane.env", "restore.sh")


class PlaneDownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.script_dir = self.root / "checkout" / "servers" / "plane"
        self.script_dir.mkdir(parents=True)
        shutil.copy2(SCRIPT, self.script_dir / "download.sh")
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        self.count_file = self.root / "curl-count"
        self._install_mock_curl()
        self.env = dict(os.environ)
        self.env.update(
            PATH=f"{self.bin_dir}{os.pathsep}{self.env['PATH']}",
            CURL_COUNT_FILE=str(self.count_file),
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def _install_mock_curl(self):
        mock = self.bin_dir / "curl"
        mock.write_text("#!/bin/sh\nset -eu\ncount=0\n[ ! -f \"$CURL_COUNT_FILE\" ] || count=$(cat \"$CURL_COUNT_FILE\")\ncount=$((count + 1))\nprintf '%s' \"$count\" > \"$CURL_COUNT_FILE\"\n[ \"${FAIL_ON_CALL:-0}\" -ne \"$count\" ] || exit 22\nwhile [ \"$#\" -gt 0 ]; do\n  if [ \"$1\" = \"-o\" ]; then shift; output=$1; fi\n  shift\ndone\nprintf 'fetched-%s\\n' \"$count\" > \"$output\"\n")
        mock.chmod(0o755)

    @property
    def install_dir(self):
        return self.script_dir / "plane-app"

    def run_downloader(self, env):
        return subprocess.run(
            ["sh", str(self.script_dir / "download.sh")],
            cwd=self.root,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_resolves_install_dir_without_git_metadata_and_preserves_filenames(self):
        result = self.run_downloader(self.env)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(path.name for path in self.install_dir.iterdir()), sorted(NAMES))
        self.assertEqual(
            [(self.install_dir / name).read_text().strip() for name in NAMES],
            ["fetched-1", "fetched-2", "fetched-3"],
        )
        self.assertFalse((self.root / ".git").exists())

    def test_failed_fetch_preserves_existing_files(self):
        self.install_dir.mkdir()
        for name in NAMES:
            (self.install_dir / name).write_text("existing content")
        self.count_file.write_text("0")
        env = dict(self.env, FAIL_ON_CALL="2")

        result = self.run_downloader(env)

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(all((self.install_dir / name).read_text() == "existing content" for name in NAMES))
        self.assertFalse(list(self.install_dir.glob(".download.*")))


if __name__ == "__main__":
    unittest.main()
