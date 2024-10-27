import os
import unittest
from unittest.mock import patch, MagicMock
from main import app, DB_PASSWORD
from cryptography.fernet import Fernet
import pyarrow as pa
import pyarrow.parquet as pq

class TestEventViewer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.setup_test_db()

    @classmethod
    def setup_test_db(cls):
        # Create a valid Fernet key
        key = Fernet.generate_key()
        fernet = Fernet(key)
        
        users_data = pa.table({'id': [1, 2], 'name': ['Alice', 'Bob'], 'email': ['alice@test.com', 'bob@test.com']})
        events_data = pa.table({'id': [1, 2], 'name': ['Event 1', 'Event 2'], 'date': ['2023-01-01', '2023-02-01']})
        participants_data = pa.table({'id': [1, 2], 'user_id': [1, 2], 'event_id': [1, 2]})
        
        for name, data in [('users', users_data), ('events', events_data), ('participants', participants_data)]:
            buffer = pa.BufferOutputStream()
            pq.write_table(data, buffer)
            encrypted_data = fernet.encrypt(buffer.getvalue().to_pybytes())
            with open(f'database/{name}.parquet', 'wb') as f:
                f.write(encrypted_data)

    # User tests
    @patch('main.get_db')
    def test_read_users(self, mock_get_db):
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchall.return_value = [(1, 'Alice', 'alice@test.com'), (2, 'Bob', 'bob@test.com')]
        mock_get_db.return_value = mock_db

        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    @patch('main.get_db')
    def test_create_user(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        new_user = {"id": 3, "name": "Charlie", "email": "charlie@test.com"}
        response = self.client.post("/users", json=new_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), new_user)

    @patch('main.get_db')
    def test_update_user(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        updated_user = {"id": 1, "name": "Alice Updated", "email": "alice_updated@test.com"}
        response = self.client.put("/users/1", json=updated_user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), updated_user)

    @patch('main.get_db')
    def test_delete_user(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        response = self.client.delete("/users/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "User deleted"})

    # Event tests
    @patch('main.get_db')
    def test_read_events(self, mock_get_db):
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchall.return_value = [(1, 'Event 1', '2023-01-01'), (2, 'Event 2', '2023-02-01')]
        mock_get_db.return_value = mock_db

        response = self.client.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    @patch('main.get_db')
    def test_create_event(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        new_event = {"id": 3, "name": "Event 3", "date": "2023-03-01"}
        response = self.client.post("/events", json=new_event)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), new_event)

    @patch('main.get_db')
    def test_update_event(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        updated_event = {"id": 1, "name": "Event 1 Updated", "date": "2023-01-02"}
        response = self.client.put("/events/1", json=updated_event)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), updated_event)

    @patch('main.get_db')
    def test_delete_event(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        response = self.client.delete("/events/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Event deleted"})

    # Participant tests
    @patch('main.get_db')
    def test_read_participants(self, mock_get_db):
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchall.return_value = [(1, 1, 1), (2, 2, 2)]
        mock_get_db.return_value = mock_db

        response = self.client.get("/participants")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    @patch('main.get_db')
    def test_create_participant(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        new_participant = {"id": 3, "user_id": 1, "event_id": 2}
        response = self.client.post("/participants", json=new_participant)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), new_participant)

    @patch('main.get_db')
    def test_update_participant(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        updated_participant = {"id": 1, "user_id": 2, "event_id": 1}
        response = self.client.put("/participants/1", json=updated_participant)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), updated_participant)

    @patch('main.get_db')
    def test_delete_participant(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        response = self.client.delete("/participants/2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Participant deleted"})

    @patch('main.get_db')
    def test_access_denied(self, mock_get_db):
        # Simulate a database error
        mock_db = MagicMock()
        mock_db.execute.side_effect = Exception("Access denied")
        mock_get_db.return_value = mock_db

        response = self.client.get("/users")
        self.assertEqual(response.status_code, 500)

if __name__ == "__main__":
    unittest.main()
