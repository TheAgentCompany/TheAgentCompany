import os
import sys
import tempfile
import threading
import types
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))
sys.modules.setdefault('litellm', types.ModuleType('litellm'))
rocketchat_api = types.ModuleType('rocketchat_API')
rocketchat_api.rocketchat = types.SimpleNamespace(RocketChat=object)
sys.modules.setdefault('rocketchat_API', rocketchat_api)
sys.modules.setdefault('rocketchat_API.rocketchat', rocketchat_api.rocketchat)

from common import EvaluationInfrastructureError, download_owncloud_content, grader
import eval as eval_entry


class OwnCloudDownloadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = urlsplit(self.path).path
                statuses = {
                    '/unauthorized': 401,
                    '/forbidden': 403,
                    '/missing': 404,
                    '/server-error': 503,
                    '/rate-limit': 429,
                }
                if path == '/share':
                    body = (
                        f'<a href="http://127.0.0.1:{self.server.server_port}'
                        '/download/file">Download</a>'
                    ).encode()
                    status = 200
                elif path == '/download/file':
                    body, status = b'original file contents', 200
                else:
                    body, status = b'unavailable', statuses.get(path, 404)
                self.send_response(status)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                pass

        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.output_path = os.path.join(self.temp_dir.name, 'downloaded.txt')

    def test_downloads_file_from_public_share_landing_page(self):
        @grader
        def graded_download():
            return download_owncloud_content(f'{self.base_url}/share', self.output_path)

        self.assertTrue(graded_download())
        with open(self.output_path, 'rb') as downloaded:
            self.assertEqual(downloaded.read(), b'original file contents')

    def test_downloads_direct_file_url(self):
        self.assertTrue(download_owncloud_content(
            f'{self.base_url}/download/file', self.output_path
        ))
        with open(self.output_path, 'rb') as downloaded:
            self.assertEqual(downloaded.read(), b'original file contents')

    def test_expected_invalid_share_statuses_return_false_without_creating_file(self):
        for path in ('unauthorized', 'forbidden', 'missing'):
            with self.subTest(status=path):
                self.assertFalse(download_owncloud_content(
                    f'{self.base_url}/{path}', self.output_path
                ))
                self.assertFalse(os.path.exists(self.output_path))

    def test_server_and_rate_limit_failures_propagate_through_grader_safely(self):
        @grader
        def graded_download(url):
            return download_owncloud_content(url, self.output_path)

        for path, expected_code in (('server-error', 'owncloud_http_503'),
                                    ('rate-limit', 'owncloud_http_429')):
            with self.subTest(status=path):
                url = f'{self.base_url}/{path}?share=private-token'
                with self.assertRaises(EvaluationInfrastructureError) as raised:
                    graded_download(url)
                self.assertEqual(raised.exception.code, expected_code)
                self.assertIsNotNone(raised.exception.cause)
                self.assertIs(raised.exception.__cause__, raised.exception.cause)
                self.assertNotIn('private-token', str(raised.exception))
                self.assertFalse(os.path.exists(self.output_path))

    def test_timeout_and_connection_errors_propagate_through_grader(self):
        @grader
        def graded_download():
            return download_owncloud_content('https://owncloud.invalid/download/file', self.output_path)

        import requests
        for cause in (requests.Timeout('private timeout url'),
                      requests.ConnectionError('private connection url')):
            with self.subTest(cause=type(cause).__name__), \
                    patch('common.requests.get', side_effect=cause):
                with self.assertRaises(EvaluationInfrastructureError) as raised:
                    graded_download()
                self.assertEqual(raised.exception.code, 'owncloud_transport_failure')
                self.assertIs(raised.exception.cause, cause)
                self.assertNotIn('private', str(raised.exception))

    def test_link_cannot_execute_shell_commands(self):
        sentinel = os.path.join(self.temp_dir.name, 'shell-was-executed')
        link = f'{self.base_url}/download;touch {sentinel}'

        self.assertFalse(download_owncloud_content(link, self.output_path))
        self.assertFalse(os.path.exists(sentinel))
        self.assertFalse(os.path.exists(self.output_path))


class EvaluationBoundaryTest(unittest.TestCase):
    def test_infrastructure_failure_exits_nonzero_and_logs_only_safe_diagnostics(self):
        cause = RuntimeError('private URL token and response body')
        failure = EvaluationInfrastructureError('owncloud_transport_failure', cause)
        failure.__cause__ = cause

        with patch.object(eval_entry, 'decrypt_and_execute'), \
                patch.object(eval_entry, 'grade_checkpoints', side_effect=failure, create=True), \
                patch('eval.sys.argv', ['eval.py']), \
                self.assertLogs(level='ERROR') as captured:
            with self.assertRaises(SystemExit) as raised:
                eval_entry.main()

        self.assertEqual(raised.exception.code, 1)
        diagnostics = '\n'.join(captured.output)
        self.assertIn('owncloud_transport_failure', diagnostics)
        self.assertIn('cause_type=RuntimeError', diagnostics)
        self.assertIn('Traceback', diagnostics)
        self.assertNotIn('private URL token', diagnostics)
        self.assertNotIn('response body', diagnostics)
        self.assertIs(failure.__cause__, cause)


if __name__ == '__main__':
    unittest.main()
