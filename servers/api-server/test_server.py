import unittest
from unittest.mock import patch
from server import app
import logging

class TestServerLogging(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('server.logger')
    def test_healthcheck_logging(self, mock_logger):
        """Test that healthcheck endpoints log correctly"""
        response = self.app.get('/api/healthcheck/gitlab')
        # Since service is likely not running during test, it should log a warning
        mock_logger.warning.assert_called_with("Web service is not available yet. Retrying...")

    @patch('server.logger')
    def test_command_execution_logging(self, mock_logger):
        """Test that command execution is logged"""
        response = self.app.post('/api/reset-rocketchat')
        mock_logger.info.assert_called_with("Executing command in /workspace/servers: make reset-rocketchat")

if __name__ == '__main__':
    unittest.main()
