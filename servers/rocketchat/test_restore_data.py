import unittest
from unittest.mock import patch, Mock
import requests
from restore_data import wait_for_rocketchat

class TestRestoreData(unittest.TestCase):
    @patch('requests.get')
    @patch('time.sleep')  # Patch sleep to avoid waiting
    def test_wait_for_rocketchat_success(self, mock_sleep, mock_get):
        """Test successful RocketChat service startup logging"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with patch('restore_data.logger') as mock_logger:
            wait_for_rocketchat(retries=1, delay=0)
            mock_logger.info.assert_called_with("Web service is up!")

    @patch('requests.get')
    @patch('time.sleep')  # Patch sleep to avoid waiting
    def test_wait_for_rocketchat_failure(self, mock_sleep, mock_get):
        """Test RocketChat service failure logging"""
        mock_get.side_effect = requests.ConnectionError()
        
        with patch('restore_data.logger') as mock_logger:
            wait_for_rocketchat(retries=1, delay=0)
            mock_logger.warning.assert_called_with("Web service is not available yet. Retrying...")

if __name__ == '__main__':
    unittest.main()

